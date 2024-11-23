from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Define choices for age categories
AGE_CHOICES = [
    ('All', 'All'),
    ('Kids', 'Kids'),
]

# Define choices for movie types
MOVIE_CHOICES = [
    ('seasonal', 'Seasonal'),
    ('single', 'Single'),
]

# Custom user model extending Django's AbstractUser
class CustomUser(AbstractUser):
    # Many-to-many relationship with Profile model
    profiles = models.ManyToManyField('Profile', blank=True)

# Profile model to represent user profiles
class Profile(models.Model):
    name = models.CharField(max_length=200)
    age_limit = models.CharField(max_length=5, choices=AGE_CHOICES)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.name

# Movie model to represent movies in the database
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.CharField(max_length=50, choices=MOVIE_CHOICES)
    video = models.ManyToManyField('Video')
    image = models.ImageField(upload_to='covers/')
    age_limit = models.CharField(max_length=5, choices=AGE_CHOICES)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200, unique=True)
    file = models.FileField(upload_to='movies/')

    def __str__(self):
        # Returns the title of the video as its string representation
        return self.title
