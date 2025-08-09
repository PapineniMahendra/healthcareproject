"""from django.contrib import admin
from healthcareapp.models import CustomUser
# Register your models here.
admin.site.register(CustomUser)"""
# healthcareapp/admin.py
from django.contrib import admin
from .models import CustomUser, BlogCategory, BlogPost

admin.site.register(CustomUser)
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
