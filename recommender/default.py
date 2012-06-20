from django.utils.functional import LazyObject
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

def get_module_class(class_path):
    try:
        mod_name, cls_name = class_path.rsplit('.', 1)
        mod = import_module(mod_name)
    except ImportError, e:
        raise ImproperlyConfigured(('Error importing module %s: "%s"' %
                                   (mod_name, e)))
    return getattr(mod, cls_name)

class Backend(LazyObject):
    def _setup(self):
        try:
            backend = settings.RECOMMENDER_BACKEND
        except:
            backend = 'recommender.backends.voting_tagging.Backend'
        self._wrapped = get_module_class(backend)()

backend = Backend()
