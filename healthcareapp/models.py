from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Automatically create categories after migration
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == __name__.split('.')[0]:  # Run only for this app
        default_categories = ["Mental Health", "Heart Disease", "Covid19", "Immunization"]
        for cat in default_categories:
            BlogCategory.objects.get_or_create(name=cat)
