
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.models import BaseUserManager

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



class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model where email is the unique identifier.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with all privileges."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, null=True, blank=True)  # ISO 3166-1 alpha-3 code

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    intrested_topics = models.ManyToManyField(IntrestedTopic, blank=True)  # Many-to-many relationship for interested topics
    lable = models.CharField(max_length=100, blank=True, null=True)
    year_of_graduation = models.IntegerField(blank=True, null=True)
    year_of_entry = models.IntegerField(blank=True, null=True)
    work = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    is_open_to_be_mentor = models.BooleanField(default=False)
    email = models.EmailField(unique=True)  # Added unique constraint for email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Removed 'email' from REQUIRED_FIELDS

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """Ensure password is hashed before saving."""
        if self.pk is None or not self.password.startswith("pbkdf2_"):  # Check if password is already hashed
            self.set_password(self.password)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.email



class PaymentGateway(models.Model):
    GATEWAY_CHOICES = [
        ("razorpay", "Razorpay"),
        ("ccavenue", "CCAvenue"),
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
    ]

    name = models.CharField(max_length=100, unique=True, choices=GATEWAY_CHOICES)
    description = models.TextField(null=True, blank=True)
    credentials = models.JSONField()  # Stores gateway-specific credentials as JSON
    is_active = models.BooleanField(default=True)

    def get_credentials(self):
        """Returns credentials dictionary."""
        return self.credentials

    def __str__(self):
        return self.name