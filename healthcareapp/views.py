# # from django.shortcuts import render, redirect
# # from django.contrib.auth import authenticate, login
# # from .forms import SignUpForm
# # from django.contrib.auth.decorators import login_required
# # from .models import CustomUser
# #
# # def home(request):
# #     return render(request, 'healthcareapp/home.html')
# #
# # def signup_view(request):
# #     if request.method == 'POST':
# #         form = SignUpForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             user = form.save()
# #             login(request, user)
# #             if user.user_type == 'patient':
# #                 return redirect('patient_dashboard')
# #             else:
# #                 return redirect('doctor_dashboard')
# #     else:
# #         form = SignUpForm()
# #     return render(request, 'healthcareapp/signup.html', {'form': form})
# #
# # def login_view(request):
# #     if request.method == 'POST':
# #         username = request.POST['username']
# #         password = request.POST['password']
# #         user = authenticate(request, username=username, password=password)
# #         if user:
# #             login(request, user)
# #             if user.user_type == 'patient':
# #                 return redirect('patient_dashboard')
# #             else:
# #                 return redirect('doctor_dashboard')
# #         else:
# #             return render(request, 'healthcareapp/login.html', {'error': 'Invalid credentials'})
# #     return render(request, 'healthcareapp/login.html')
# #
# # @login_required
# # def patient_dashboard(request):
# #     return render(request, 'healthcareapp/patient_dashboard.html')
# #
# # @login_required
# # def doctor_dashboard(request):
# #     return render(request, 'healthcareapp/doctor_dashboard.html')
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from .forms import SignUpForm
# from django.contrib.auth.decorators import login_required
# from .models import CustomUser
# from django.contrib import messages  # ✅ added for optional success message
#
# def home(request):
#     return render(request, 'healthcareapp/home.html')
#
# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Registration successful! Please log in.")  # ✅ optional message
#             return redirect('login')  # ✅ redirect to login instead of dashboard
#     else:
#         form = SignUpForm()
#     return render(request, 'healthcareapp/signup.html', {'form': form})
#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             if user.user_type == 'patient':
#                 return redirect('patient_dashboard')
#             else:
#                 return redirect('doctor_dashboard')
#         else:
#             return render(request, 'healthcareapp/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'healthcareapp/login.html')
#
# @login_required
# def patient_dashboard(request):
#     return render(request, 'healthcareapp/patient_dashboard.html')
#
# @login_required
# def doctor_dashboard(request):
#     return render(request, 'healthcareapp/doctor_dashboard.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib import messages

def home(request):
    return render(request, 'healthcareapp/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'healthcareapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
        else:
            return render(request, 'healthcareapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'healthcareapp/login.html')

@login_required
def patient_dashboard(request):
    return render(request, 'healthcareapp/patient_dashboard.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'healthcareapp/doctor_dashboard.html')

# ✅ Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
