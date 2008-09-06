from django.db import models

# Create your models here.
from recommender.managers import RecommenderManager


class Recommender(models.Model):

    objects = RecommenderManager()

class TestItem(models.Model):

    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return '%s' % self.name
