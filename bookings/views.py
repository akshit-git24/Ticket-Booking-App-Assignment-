from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
# Create your views here.
def homepage(request):
    return render(request, 'Homepage.html')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '🎉 Welcome to Travel Haven! Your account has been created successfully.')
            return redirect('combined_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'Registeration_Form.html', {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}! 👋')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()    
    return render(request, 'LoginForm.html', {"form": form})  


def logout_view(request):
    messages.success(request, 'You have been logged out successfully. See you soon! 👋')
    logout(request)
    return redirect('homepage')