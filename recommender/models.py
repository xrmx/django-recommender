from django.db import models

from recommender.managers import RecommenderManager

# Main recommender class. Add here whatever you need to be parametrizable: min values, weigths...
class Recommender(models.Model):

    objects = RecommenderManager()
