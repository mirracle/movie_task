from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre)
    release_year = models.PositiveIntegerField()
    likes = models.ManyToManyField(User, related_name='liked_movies')
