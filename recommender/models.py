from django.db import models

from recommender.managers import RecommenderManager

class Recommender(models.Model):
    objects = RecommenderManager()

    class Meta:
        abstract = True
