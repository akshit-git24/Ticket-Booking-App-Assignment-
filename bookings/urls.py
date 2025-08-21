from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('travel-options/', views.travel_options, name='travel_options'),
    path('book/<int:travel_id>/', views.book_travel, name='book_travel'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]