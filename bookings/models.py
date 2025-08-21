from django.db import models

# Create your models here.

class TravelOption(models.Model):
    TRAVEL_TYPES = [('flight', 'Flight ✈️'),('train', 'Train 🚆'),('bus', 'Bus 🚌')]
    STATUS_CHOICES = [('available', 'Available ✅'),('full', 'Fully Booked 🔴'),('cancelled', 'Cancelled ❌')]
    
    travel_id = models.AutoField(primary_key=True, verbose_name="Travel ID")
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES, verbose_name="Travel Type", help_text="Choose your transport Mode")
    source = models.CharField(max_length=100, verbose_name="From City", help_text="Departure city")
    destination = models.CharField(max_length=100, verbose_name="To City", help_text="Arrival city")
    departure_date = models.DateField(verbose_name="Departure Date", help_text="When does the journey start?")
    departure_time = models.TimeField(verbose_name="Departure Time", help_text="What time does it leave?")
    arrival_date = models.DateField(verbose_name="Arrival Date", help_text="When will you reach?")
    arrival_time = models.TimeField(verbose_name="Arrival Time", help_text="What time will you arrive?")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price per Seat", help_text="Cost for one person")
    available_seats = models.PositiveIntegerField(verbose_name="Available Seats", help_text="How many seats are left?")
    total_seats = models.PositiveIntegerField(verbose_name="Total Seats", help_text="Maximum capacity")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available', verbose_name="Booking Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Added On")
    
    def __str__(self):
        return f"{self.get_type_display()} from {self.source} to {self.destination} on {self.departure_date}"
    
    class Meta:
        ordering = ['departure_date', 'departure_time']
        verbose_name = "Travel Option"
        verbose_name_plural = "Travel Options"