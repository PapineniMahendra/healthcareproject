
from django.urls import path
from . import views

urlpatterns = [
    # Existing routes
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

    # ----------------------------
    # 📌 Blog feature routes (Task 2)
    # ----------------------------
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('categories/', views.categories_view, name='categories'),
    path('category/<int:category_id>/', views.category_blogs, name='category_blogs'),

]
