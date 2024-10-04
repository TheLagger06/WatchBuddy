from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_picture = models.URLField(blank=True, null=True)  # Assuming a URL for profile pictures

    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Fields required on registration

    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change this to a unique name
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change this to a unique name
        blank=True,
    )

    def __str__(self):
        return self.email


class MovieSeries(models.Model):
    """Model for Movies and Series."""
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # e.g., 8.5

    def __str__(self):
        return self.title

class Favorites(models.Model):
    """Model for User Favorites."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie_series = models.ForeignKey(MovieSeries, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie_series')  # Ensures a user can favorite a movie/series only once

class Comment(models.Model):
    """Model for User Comments."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie_series = models.ForeignKey(MovieSeries, on_delete=models.CASCADE)
    comment_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.comment_text[:20]}..."

class Tracking(models.Model):
    """Model for Tracking Movie/Series Progress."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie_series = models.ForeignKey(MovieSeries, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)  # Whether the user has watched it
    progress = models.IntegerField(default=0)  # Number of episodes watched (for series)

    def __str__(self):
        return f"{self.user.email} is tracking {self.movie_series.title}"

