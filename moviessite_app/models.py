from django.db import models

RATING = (
    (1, 1.0),
    (2, 1.5),
    (3, 2.0),
    (4, 2.5),
    (5, 3.0),
    (6, 3.5),
    (7, 4.0),
    (8, 4.5),
    (9, 5.0)
)


class Actor(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    description = models.TextField(null=True)
    rating = models.IntegerField(choices=RATING)


class Director(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    description = models.TextField(null=True)
    rating = models.IntegerField(choices=RATING)


class Movie(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True)
    rating = models.IntegerField(choices=RATING)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)


class ActorMovie(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    description = models.TextField()

