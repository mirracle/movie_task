from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Movie(models.Model):
    name = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre)
    year = models.PositiveIntegerField()
    likes = models.ManyToManyField(User, related_name='liked_movies')
