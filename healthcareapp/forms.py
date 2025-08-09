
from django import forms
from .models import CustomUser, BlogPost
from django.contrib.auth.forms import UserCreationForm

# -----------------------------
# User Registration Form
# -----------------------------
class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'user_type',
            'profile_picture', 'address_line1', 'city', 'state', 'pincode'
        ]


# -----------------------------
# Blog Post Creation Form (for Doctors)
# -----------------------------
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'is_draft']
