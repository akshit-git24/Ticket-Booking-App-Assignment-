from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import TravelOption
from datetime import datetime, date
# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '🎉 Welcome to Travel Haven! Your account has been created successfully.')
            return redirect('homepage')
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
    return render(request, 'loginForm.html', {"form": form})  


def logout_view(request):
    messages.success(request, 'You have been logged out successfully. See you soon! 👋')
    logout(request)
    return redirect('homepage')

def travel_options(request):
    travel_type = request.GET.get('type')  
    source_city = request.GET.get('source') 
    destination_city = request.GET.get('destination')  
    travel_date = request.GET.get('date')  
    
    if travel_type and source_city and destination_city and travel_date:
        available_options = TravelOption.objects.filter(status='available').order_by('departure_date', 'departure_time')
        show_results = True
        is_filtered = True
        available_options = available_options.filter(type=travel_type,source=source_city,destination=destination_city)
        
        try:
            date = datetime.strptime(travel_date, '%Y-%m-%d').date()
            available_options = available_options.filter(departure_date=date)
        except ValueError:
            available_options = TravelOption.objects.none()
            messages.error(request, '❌ Please enter a valid date format')
    else:
        available_options = TravelOption.objects.none()
        show_results = False
        is_filtered = False
        
        if request.GET: 
            messages.warning(request, ' ⚠️ Please fill in all search fields to find Your desired travel options')
    
    all_sources = TravelOption.objects.values_list('source', flat=True).distinct().order_by('source')
    all_destinations = TravelOption.objects.values_list('destination', flat=True).distinct().order_by('destination')
    
    context = {'travel_options': available_options,'sources': all_sources,'destinations': all_destinations,'selected_type': travel_type,'selected_source': source_city,
            'selected_destination': destination_city,'selected_date': travel_date,'show_results': show_results,'is_filtered': is_filtered,'total_options': available_options.count(),}
    
    return render(request, 'travel_options.html', context) 


