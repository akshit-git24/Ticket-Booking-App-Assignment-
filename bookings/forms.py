from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','phone_number', 'date_of_birth', 'address', 'city', 'state', 'country', 'postal_code', 'emergency_contact_name','emergency_contact_phone']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*',}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '📱 +91 XXXXXXXXXX'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '🏠 Enter your complete address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '🏙️ Your city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '🗺️ State or Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '🌍 Country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '📮 Postal Code'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '👤 Emergency contact name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '📞 Emergency contact number'}),}

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),}