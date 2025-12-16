# MeroPanditLama Backend

Django REST API for connecting users with Hindu Pandits and Buddhist Lamas.

## Quick Start

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file (copy from setup.md)

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Load initial data:
```bash
python manage.py shell < load_services.py
```

7. Run server:
```bash
python manage.py runserver
```

## API Documentation

### Authentication
- POST `/api/auth/signup/` - Register user
- POST `/api/auth/login/` - Login (returns role for redirect)
- POST `/api/auth/refresh/` - Refresh token
- GET `/api/profile/` - Get profile
- PUT `/api/profile/` - Update profile

### Providers (Public)
- GET `/api/providers/` - List providers
- GET `/api/providers/{id}/` - Provider details
- GET `/api/providers/{id}/availability/` - Check availability

### Provider Dashboard (Provider role only)
- GET `/api/provider/dashboard/` - Dashboard stats
- GET `/api/provider/bookings/` - My booking requests
- GET `/api/provider/profile/` - My profile
- PUT `/api/provider/profile/` - Update profile
- POST `/api/provider/availability/` - Set availability
- GET `/api/provider/availability/` - My availability

### Bookings
- POST `/api/bookings/` - Create booking (User)
- GET `/api/bookings/` - List bookings
- GET `/api/bookings/{id}/` - Booking details
- POST `/api/bookings/{id}/confirm/` - Confirm (Provider)
- POST `/api/bookings/{id}/reject/` - Reject (Provider)
- POST `/api/bookings/{id}/cancel/` - Cancel (Both)
- POST `/api/bookings/{id}/complete/` - Mark complete (Provider)

### Admin Panel
- `/admin/` - Django admin (create providers here)