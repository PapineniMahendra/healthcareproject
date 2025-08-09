from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, BlogPost, BlogCategory
from django.contrib import messages
from django.http import Http404


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

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def blog_list(request):
    """
    Patient & general view - shows only published blogs category-wise.
    """
    categories = BlogCategory.objects.all().order_by('name')
    category_posts = []

    for cat in categories:
        posts = BlogPost.objects.filter(category=cat, is_draft=False).order_by('-created_at')
        category_posts.append((cat, posts))

    return render(request, 'healthcareapp/blog_list.html', {'category_posts': category_posts})


@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    # Restrict draft view to the author only
    if blog.is_draft:
        if not request.user.is_authenticated or request.user != blog.author:
            raise Http404

    return render(request, 'healthcareapp/blog_detail.html', {'blog': blog})


@login_required
def blog_create(request):
    """
    Allows doctors to create blog posts with draft support.
    """
    if request.user.user_type != 'doctor':
        messages.error(request, "Only doctors can create blog posts.")
        return redirect('blog_list')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        summary = request.POST.get('summary', '').strip()
        content = request.POST.get('content', '').strip()
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        is_draft = True if request.POST.get('is_draft') == 'on' else False

        if not title or not content or not category_id:
            messages.error(request, "Please fill Title, Category and Content.")
            categories = BlogCategory.objects.all()
            return render(request, 'healthcareapp/blog_create.html', {'categories': categories})

        category = get_object_or_404(BlogCategory, id=category_id)

        BlogPost.objects.create(
            title=title,
            summary=summary,
            content=content,
            category=category,
            image=image,
            author=request.user,
            is_draft=is_draft
        )

        if is_draft:
            messages.success(request, "Draft saved successfully.")
        else:
            messages.success(request, "Blog published successfully.")

        return redirect('my_blogs')

    categories = BlogCategory.objects.all()
    return render(request, 'healthcareapp/blog_create.html', {'categories': categories})


@login_required
def my_blogs(request):
    """
    Shows all blogs (draft & published) of the logged-in doctor.
    """
    if request.user.user_type != 'doctor':
        return redirect('blog_list')

    blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'healthcareapp/my_blogs.html', {'blogs': blogs})
@login_required
def categories_view(request):
    """
    Shows all blog categories (for patients to browse).
    """
    categories = BlogCategory.objects.all().order_by('name')
    return render(request, 'healthcareapp/categories.html', {'categories': categories})
@login_required
def category_blogs(request, category_id):
    """
    Shows all published (non-draft) blogs from all doctors in the given category.
    """
    category = get_object_or_404(BlogCategory, id=category_id)
    blogs = BlogPost.objects.filter(category=category, is_draft=False).order_by('-created_at')

    return render(request, 'healthcareapp/category_blogs.html', {
        'category': category,
        'blogs': blogs
    })
