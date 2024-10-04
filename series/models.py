from django.db import models

class Series(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster_path = models.CharField(max_length=255)
    backdrop_path = models.CharField(max_length=255)
    release_date = models.DateField()
    rating = models.FloatField()

    def __str__(self):
        return self.title
