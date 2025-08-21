# 🧳 Travel Booking Application

A simple and user-friendly travel booking web application built with **Python (Django)**.  
The app allows **authenticated users** to browse travel options (Flights, Trains, Buses), book tickets, and manage their bookings.

---

## 🚀 Features

### 🔐 User Management
- User registration, login, and logout using Django authentication.  
- Profile management: update user details.  
- Only authenticated users can make bookings.  

### 🚌 Travel Options
- Travel types: **Flights, Trains, Buses**  
- Each option includes:  
  - Travel ID  
  - Type (Flight, Train, Bus)  
  - Source & Destination  
  - Date & Time  
  - Price  
  - Available Seats  

### 🎫 Booking System
- Users can book tickets with seat availability validation.  
- Booking data includes:  
  - Booking ID  
  - User (FK)  
  - Travel Option (FK)  
  - Seats  
  - Total Price  
  - Booking Date  
  - Status (Confirmed / Cancelled)  
- Manage bookings: view current/past bookings, cancel reservations.  

### 🎨 Frontend (Django Templates + CSS/Bootstrap)
- Pages for:
  - Registration, Login, Profile  
  - Viewing travel options (with filters: type, source, destination, date)  
  - Booking tickets  
  - Managing bookings  
- Responsive design for desktop and mobile.  

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** Django Templates, HTML, CSS, Bootstrap  
- **Database:** SQLite (default) or MySQL  
- **Deployment:** AWS / any cloud (optional)  

---

## ⚡ Quickstart

### 1. Clone
```bash
git clone https://github.com/<your-username>/travel-booking-app.git
cd travel-booking-app
```
2. Setup Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```
3. Database Setup
MySQL (recommended)
Update settings.py:
```bash
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'travel_db',
    'USER': 'your_username',
    'PASSWORD': 'your_password',
    'HOST': 'localhost',
    'PORT': '3306',
  }
}
Then run:
#after configration
python manage.py makemigrations
python manage.py migrate
```
4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
5. Run Server
```bash
python manage.py runserver
App will be available at: http://127.0.0.1:8000/
```

🌍 Deployment
Set DEBUG=False in production.

Configure ALLOWED_HOSTS.

Use collectstatic for static files.

Deployed on Render and database hosted on Railway.

📂 Data Models
TravelOption
travel_id (Auto/UUID)

type (Flight / Train / Bus)

source, destination

date_time

price

available_seats

Booking
booking_id (Auto/UUID)

user (ForeignKey)

travel_option (ForeignKey)

seats

total_price

booking_date

status (Confirmed / Cancelled)

👨‍💻 Contributors
Akshit Sahore
