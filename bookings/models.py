from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

class TravelOption(models.Model):
    TRAVEL_TYPES = [('flight', 'Flight ✈️'),('train', 'Train 🚆'),('bus', 'Bus 🚌')]
    STATUS_CHOICES = [('available', 'Available ✅'),('full', 'Fully Booked 🔴'),('cancelled', 'Cancelled ❌')]
    
    travel_id = models.AutoField(primary_key=True, verbose_name="Travel ID")
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES, verbose_name="Travel Type", help_text="Choose your transport Mode")
    source = models.CharField(max_length=100, verbose_name="From City", help_text="Departure city")
    destination = models.CharField(max_length=100, verbose_name="To City", help_text="Arrival city")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Added On")
    departure_date = models.DateField(verbose_name="Departure Date", help_text="When does the journey start?")
    departure_time = models.TimeField(verbose_name="Departure Time", help_text="What time does it leave?")
    arrival_date = models.DateField(verbose_name="Arrival Date", help_text="When will you reach?")
    arrival_time = models.TimeField(verbose_name="Arrival Time", help_text="What time will you arrive?")
    total_seats = models.PositiveIntegerField(verbose_name="Total Seats", help_text="Maximum capacity")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price per Seat", help_text="Cost for one person")
    available_seats = models.PositiveIntegerField(verbose_name="Available Seats", help_text="How many seats are left?")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available', verbose_name="Booking Status")
    
    def __str__(self):
        return f"{self.get_type_display()} from {self.source} to {self.destination} on {self.departure_date}"
    
    class Meta:
        ordering = ['departure_date', 'departure_time']
        


class Booking(models.Model):
    BOOKING_STATUS = [('confirmed', 'Confirmed ✅'),('cancelled', 'Cancelled ❌'),('pending', 'Pending ⏳')]
    
    booking_id = models.AutoField(primary_key=True, verbose_name="Booking ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="Customer", help_text="Who made this booking?")
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE, related_name='bookings', verbose_name="Travel Details", help_text="Which travel option was booked?")
    number_of_seats = models.PositiveIntegerField(verbose_name="Number of Seats", help_text="How many seats were booked?")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount", help_text="Total cost for all seats")
    booking_date = models.DateTimeField(default=timezone.now, verbose_name="Booked On", help_text="When was this booking made?")
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='confirmed', verbose_name="Booking Status")
    passenger_details = models.JSONField(default=dict, blank=True, verbose_name="Passenger Information", help_text="Additional passenger details")
    
    def __str__(self):
        return f"Booking #{self.booking_id} - {self.user.get_full_name() or self.user.username} - {self.travel_option.source} to {self.travel_option.destination}"
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.travel_option.price * self.number_of_seats
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-booking_date']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="User Account")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Profile Picture",help_text="Upload your profile picture")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Phone Number", help_text="Your contact number for booking updates")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth", help_text="When were you born?")
    address = models.TextField(blank=True, verbose_name="Home Address", help_text="Your complete address")
    city = models.CharField(max_length=100, blank=True, verbose_name="City", help_text="Which city do you live in?")
    state = models.CharField(max_length=100, blank=True, verbose_name="State/Province", help_text="Your state or province")
    country = models.CharField(max_length=100, blank=True, default="India", verbose_name="Country", help_text="Which country are you from?")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="Postal Code", help_text="Your area postal code")
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name="Emergency Contact Name", help_text="Someone to contact in case of emergency")
    emergency_contact_phone = models.CharField(max_length=15, blank=True, verbose_name="Emergency Contact Phone", help_text="Emergency contact's phone number")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Profile Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    def __str__(self):
        return f"{self.get_full_name()}'s Travel Profile"
    
    def get_full_name(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name if full_name else self.user.username
    
    def is_complete(self):
        return bool(self.phone_number and self.address and self.city)
    
    def delete(self, *args, **kwargs):
        if self.profile_picture:
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
        super().delete(*args, **kwargs)
    