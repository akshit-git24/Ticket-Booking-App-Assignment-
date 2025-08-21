from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import TravelOption,Booking,UserProfile
from datetime import datetime, date
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm,UserProfileUpdateForm
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
        available_options = TravelOption.objects.filter(status='available').order_by('departure_date', 'departure_time')[:10]
        show_results = False
        is_filtered = False
        
        if request.GET: 
            messages.warning(request, ' ⚠️ Please fill in all search fields to find Your desired travel options')
    
    all_sources = TravelOption.objects.values_list('source', flat=True).distinct().order_by('source')
    all_destinations = TravelOption.objects.values_list('destination', flat=True).distinct().order_by('destination')
    
    context = {'travel_options': available_options,'sources': all_sources,'destinations': all_destinations,'selected_type': travel_type,'selected_source': source_city,
            'selected_destination': destination_city,'selected_date': travel_date,'show_results': show_results,'is_filtered': is_filtered,'total_options': available_options.count(),}
    
    return render(request, 'travel_options.html', context) 

@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id, status='available')
    if request.method == 'POST':
        requested_seats = int(request.POST.get('seats', 1))
        if requested_seats > travel_option.available_seats:
            messages.error(request, f'❌ Sorry! Only {travel_option.available_seats} seats are available for this trip.')
            return redirect('book_travel', travel_id=travel_id)
        
        new_booking = Booking.objects.create(user=request.user,travel_option=travel_option,number_of_seats=requested_seats,total_price=travel_option.price * requested_seats)
        travel_option.available_seats -= requested_seats

        if travel_option.available_seats == 0:
            travel_option.status = 'full' 

        travel_option.save()
        messages.success(request, f'🎉 Booking confirmed! Your booking ID is #{new_booking.booking_id}. Have a great trip!')
        return redirect('my_bookings')
    
    context = {'travel_option': travel_option,'max_seats': min(travel_option.available_seats, 10)}

    return render(request, 'book_travel.html', context)

@login_required
def my_bookings(request):
    user_bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': user_bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if booking.status == 'cancelled':
        messages.warning(request, 'Booking is already cancelled!')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        travel_option = booking.travel_option
        travel_option.available_seats += booking.number_of_seats
        if travel_option.status == 'full':
            travel_option.status = 'available'
        travel_option.save()
        
        messages.success(request, 'Your Booking cancelled successfully!')
        return redirect('my_bookings')
    
    return render(request, 'cancel_booking.html', {'booking': booking})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if booking.status != 'cancelled':
        messages.error(request, 'Only cancelled bookings can be deleted!')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully!')
        return redirect('my_bookings')
    
    return render(request, 'delete_booking.html', {'booking': booking})

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    recent_bookings = Booking.objects.filter(user=request.user)[:5]
    total_bookings = Booking.objects.filter(user=request.user).count()
    confirmed_bookings = Booking.objects.filter(user=request.user, status='confirmed').count()
    cancelled_bookings = Booking.objects.filter(user=request.user, status='cancelled').count()
    current_bookings = Booking.objects.filter(user=request.user,status='confirmed',travel_option__departure_date__gte=date.today())[:3] 
    
    context = {'profile': profile,'recent_bookings': recent_bookings,'total_bookings': total_bookings,
               'confirmed_bookings': confirmed_bookings,'cancelled_bookings': cancelled_bookings,'current_bookings': current_bookings,}
    
    return render(request, 'dashboard.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile,created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileUpdateForm(instance=profile)

    return render(request, 'edit_profile.html',{'user_form': user_form,'profile_form': profile_form})

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    travel_type = request.GET.get('travel_type')
    if travel_type:
        bookings = bookings.filter(travel_option__type=travel_type)
    
    date_filter = request.GET.get('date_filter')
    if date_filter == 'upcoming':
        bookings = bookings.filter(travel_option__departure_date__gte=date.today())
    elif date_filter == 'past':
        bookings = bookings.filter(travel_option__departure_date__lt=date.today())
    
    context = {'bookings': bookings,'status_filter': status_filter,'travel_type': travel_type,'date_filter': date_filter,'today': date.today()}
    return render(request, 'booking_history.html', context)

@login_required
def create_profile(request):
    if hasattr(request.user, 'profile'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('Homepage')
    else:
        form = UserProfileUpdateForm()
    return render(request, 'create_profile.html', {'form': form})