from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
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
                request, ("Username created. Please finish your user info below"))
            return redirect('update_info')
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
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, "Profile Updated")
            return redirect('home')
        return render(request,'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in to access that page")
        return redirect('home')
    
def update_pass(request):
    if request.user.is_authenticated:
        current_user=request.user 
        
        #Did They fill out the form
        if request.method == 'POST':
            form=ChangePasswordForm(current_user, request.POST)
            #Is the form valid?
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_pass')
                            
        else:
            form = ChangePasswordForm(current_user)
    else:
        messages.success(request, "You must be logged in to access that page")
        return redirect('home')
    return render(request, 'update_pass.html', {'form':form})    

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Info Updated")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to access that page")
        return redirect('home')
    
def search(request):
    #Determina se foi feita alguma pesquisa
    if request.method == "POST":
        searched = request.POST['searched']
        #Query the Products DB model
        searched = Product.objects.filter(name__icontains=searched)
        return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html', {})
