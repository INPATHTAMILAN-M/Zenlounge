
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='university_logos/', blank=True, null=True)
    established = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class IntrestedTopic(models.Model):
    topic = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.topic


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    intrested_topics = models.ManyToManyField(IntrestedTopic, null=True, blank=True)
    year_of_entry = models.IntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=True)  # Added unique constraint for email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Removed 'email' from REQUIRED_FIELDS

    objects = UserManager()
    
    def __str__(self):
        return self.email
