from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, "You have been logged in, Welcome aboard")
            return redirect("home")
        else:
            messages.error(request, "There was an error, please try again")
            return redirect("login")
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log in User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, ("User created successifully. Welcome Aboard"))
            return redirect('home')
        else:
            messages.success(
                request, ("Wooops! There was a problem registering. Please try again"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {'product': product})


def category(request, foo):
    # Troca hifem por espaço
    foo = foo.replace('-', ' ')
    # Pega a categoria da URL
    try:
        #Procurar a categoria
        category=Category.objects.get(name=foo)
        product=Product.objects.filter(category=category)
        return render(request, 'category.html',{'products':product, 'category':category})
    except:
        messages.success(request, ("Inexistent Category"))
        return redirect(home)


def category_summary(request):
    return render(request, 'category_summary.html', {})