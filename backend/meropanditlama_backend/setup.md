# MeroPanditLama Django API Setup Instructions

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment knowledge

---

## Installation Steps

### 1. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory:
```env
# Django Configuration
SECRET_KEY=django-insecure-your-secret-key-change-in-production-make-it-very-long
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Console backend for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@meropanditlama.com

# Frontend URL (for CORS and email links)
FRONTEND_URL=http://localhost:3000

# Google OAuth (Optional - leave empty for now)
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
```

### 4. Database Setup
```bash
# Create migrations for all apps
python manage.py makemigrations accounts
python manage.py makemigrations providers
python manage.py makemigrations bookings

# Apply all migrations
python manage.py migrate
```

### 5. Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Email address: `admin@meropanditlama.com`
- Username: `admin`
- Password: (choose a secure password)
- First name: `Admin`
- Last name: `User`

### 6. Load Initial Services Data

Create a file named `load_services.py` in the root directory:
```python
from api.providers.models import Service

services = [
    {
        'name': 'Ghar Puja',
        'name_ne': 'घर पूजा',
        'description': 'House warming and purification ceremony',
        'description_ne': 'घर वार्मिंग र शुद्धीकरण समारोह',
        'default_price': 3000
    },
    {
        'name': 'Bartabanda',
        'name_ne': 'बर्तबन्द',
        'description': 'Sacred thread ceremony for young boys',
        'description_ne': 'जवान केटाहरूको लागि पवित्र धागो समारोह',
        'default_price': 5000
    },
    {
        'name': 'Bratabandha',
        'name_ne': 'ब्रतबन्ध',
        'description': 'Coming of age ceremony',
        'description_ne': 'उमेर आगमन समारोह',
        'default_price': 8000
    },
    {
        'name': 'Buddha Puja',
        'name_ne': 'बुद्ध पूजा',
        'description': 'Buddhist prayer and meditation ceremony',
        'description_ne': 'बौद्ध प्रार्थना र ध्यान समारोह',
        'default_price': 4000
    },
    {
        'name': 'Wedding Ceremony',
        'name_ne': 'विवाह समारोह',
        'description': 'Traditional wedding rituals and blessings',
        'description_ne': 'परम्परागत विवाह संस्कार र आशीर्वाद',
        'default_price': 15000
    },
    {
        'name': 'Griha Pravesh',
        'name_ne': 'गृह प्रवेश',
        'description': 'House entrance ceremony',
        'description_ne': 'घर प्रवेश समारोह',
        'default_price': 4500
    },
]

print("Loading services...")
for service_data in services:
    service, created = Service.objects.get_or_create(
        name=service_data['name'],
        defaults=service_data
    )
    if created:
        print(f"✅ Created: {service.name}")
    else:
        print(f"ℹ️  Already exists: {service.name}")

print("\n✅ All services loaded successfully!")
```

Run the script:
```bash
python manage.py shell < load_services.py
```

### 7. Start Development Server
```bash
python manage.py runserver
```

The server will start at: `http://localhost:8000/`

---

## Admin Interface

Access the admin panel at: `http://localhost:8000/admin/`

Login with the superuser credentials you created in Step 5.

---

## Adding Content

### 1. Create a Test Provider Account

Follow these steps in the admin panel:

#### Step 1: Create Provider User
1. Navigate to: **Users** → **Add User**
2. Fill in the details:
   - **Email**: `pandit@example.com`
   - **Username**: `pandit`
   - **Password**: `test123456` (click "Raw passwords are not stored" to set)
   - **Password confirmation**: `test123456`
3. Click **Save and continue editing**

#### Step 2: Set Additional User Details
1. In the **Personal Info** section:
   - **First name**: `Ram`
   - **Last name**: `Sharma`
   - **Phone**: `9841234567`
2. In the **Permissions** section:
   - **Role**: Select **Service Provider**
   - **Language preference**: `English` or `Nepali`
   - **Active**: ✓ (checked)
   - **Staff status**: Leave unchecked
3. Click **Save**

#### Step 3: Create Provider Profile
1. Navigate to: **Service Providers** → **Add Service Provider**
2. Fill in the details:
   - **User**: Select `pandit@example.com - Ram Sharma`
   - **Religion type**: `Hindu Pandit`
   - **Experience years**: `10`
   - **Location**: `Kathmandu, Bhaktapur`
   - **Short description**: `Experienced Hindu Pandit specializing in traditional ceremonies`
   - **Price per service**: `5000.00`
   - **Services**: Select multiple services (Ctrl+Click on Windows, Cmd+Click on Mac)
     - Ghar Puja
     - Bartabanda
     - Wedding Ceremony
   - **Verified**: ✓ (checked - important for provider to appear in listings)
3. Click **Save**

#### Step 4: Set Provider Availability (Optional)
1. Navigate to: **Availability Slots** → **Add Availability Slot**
2. Add available time slots:
   - **Provider**: Select the provider you just created
   - **Date**: Select a future date
   - **Start time**: `09:00:00`
   - **End time**: `11:00:00`
   - **Is booked**: Leave unchecked
3. Click **Save and add another** to add more slots

### 2. Create a Test User Account

1. Navigate to: **Users** → **Add User**
2. Fill in:
   - **Email**: `user@example.com`
   - **Username**: `testuser`
   - **Password**: `test123456`
   - **First name**: `Anjali`
   - **Last name**: `Sharma`
   - **Phone**: `9851234567`
   - **Role**: `User` (default)
3. Click **Save**

---

## API Endpoints

The API is available at: `http://localhost:8000/api/`

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup/` | Register new user | No |
| POST | `/api/auth/login/` | Login (returns role) | No |
| POST | `/api/auth/refresh/` | Refresh JWT token | No |
| GET | `/api/profile/` | Get user profile | Yes |
| PUT | `/api/profile/` | Update profile | Yes |

### Provider Endpoints (Public)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/providers/` | List all providers | No |
| GET | `/api/providers/{id}/` | Provider details | No |
| GET | `/api/providers/{id}/availability/` | Check availability | No |
| GET | `/api/services/` | List all services | No |

### Provider Dashboard (Provider Role Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/provider/dashboard/` | Dashboard stats | Yes (Provider) |
| GET | `/api/provider/bookings/` | Booking requests | Yes (Provider) |
| GET | `/api/provider/profile/` | My profile | Yes (Provider) |
| PUT | `/api/provider/profile/` | Update profile | Yes (Provider) |
| GET | `/api/provider/availability/` | My availability | Yes (Provider) |
| POST | `/api/provider/availability/` | Set availability | Yes (Provider) |

### Booking Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/bookings/` | Create booking | Yes (User) |
| GET | `/api/bookings/` | List my bookings | Yes |
| GET | `/api/bookings/{id}/` | Booking details | Yes |
| POST | `/api/bookings/{id}/confirm/` | Confirm booking | Yes (Provider) |
| POST | `/api/bookings/{id}/reject/` | Reject booking | Yes (Provider) |
| POST | `/api/bookings/{id}/cancel/` | Cancel booking | Yes |
| POST | `/api/bookings/{id}/complete/` | Mark complete | Yes (Provider) |

---

## Testing the API

### Using cURL

#### 1. Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "Sita",
    "last_name": "Rai",
    "phone": "9841234568",
    "language_pref": "ne"
  }'
```

#### 2. Login (Returns Role for Frontend Redirect)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "pandit@example.com",
    "password": "test123456"
  }'
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 2,
    "email": "pandit@example.com",
    "first_name": "Ram",
    "last_name": "Sharma",
    "role": "provider",
    "profile_photo": null
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Frontend should check `user.role`:**
- If `"provider"` → Redirect to `/provider/dashboard`
- If `"user"` → Redirect to `/user/dashboard`

#### 3. Get Providers List
```bash
curl http://localhost:8000/api/providers/
```

#### 4. Get Providers with Filters
```bash
# Filter by religion
curl "http://localhost:8000/api/providers/?religion_type=hindu"

# Filter by location
curl "http://localhost:8000/api/providers/?location=Kathmandu"

# Search
curl "http://localhost:8000/api/providers/?search=Ram"

# Multiple filters
curl "http://localhost:8000/api/providers/?religion_type=hindu&verified=true"
```

#### 5. Check Provider Availability
```bash
curl "http://localhost:8000/api/providers/1/availability/?date_from=2025-01-01&date_to=2025-01-31"
```

#### 6. Create Booking (Requires Authentication)
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "provider_id": 1,
    "service_id": 2,
    "requested_datetime": "2025-01-20T09:00:00Z",
    "duration_minutes": 120,
    "notes": "Please bring all necessary items"
  }'
```

### Using JavaScript (Frontend Integration)
```javascript
// Login and handle redirect based on role
async function login(email, password) {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  
  // Store token
  localStorage.setItem('token', data.token);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  // Redirect based on role
  if (data.user.role === 'provider') {
    window.location.href = '/provider/dashboard';
  } else {
    window.location.href = '/user/dashboard';
  }
}

// Fetch providers with authentication
async function getProviders() {
  const response = await fetch('http://localhost:8000/api/providers/?religion_type=hindu');
  const data = await response.json();
  console.log(data.results);
}

// Create booking with authentication
async function createBooking(bookingData) {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:8000/api/bookings/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(bookingData)
  });
  
  return await response.json();
}
```

---

## File Structure Overview
meropanditlama/
├── api/                        # Main API package
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py               # WSGI application
│   ├── accounts/             # User authentication
│   │   ├── models.py         # User model with roles
│   │   ├── serializers.py    # Auth serializers
│   │   ├── views.py          # Login, signup, profile
│   │   └── admin.py          # User admin interface
│   ├── providers/            # Provider management
│   │   ├── models.py         # Provider, Service, Availability
│   │   ├── serializers.py    # Provider serializers
│   │   ├── views.py          # Provider endpoints
│   │   └── admin.py          # Provider admin
│   ├── bookings/             # Booking system
│   │   ├── models.py         # Booking model
│   │   ├── serializers.py    # Booking serializers
│   │   ├── views.py          # Booking endpoints
│   │   └── admin.py          # Booking admin
│   ├── notifications/        # Email notifications
│   │   └── utils.py          # Email sending utilities
│   └── templates/            # Email templates
│       └── emails/
│           ├── booking_requested_en.html
│           └── booking_confirmed_en.html
├── media/                     # User uploads (auto-created)
│   └── profiles/             # Profile photos
├── static/                    # Static files
├── venv/                      # Virtual environment
├── .env                       # Environment variables
├── .gitignore
├── db.sqlite3                # Database (auto-created)
├── manage.py
├── readme.md
├── requirements.txt
└── setup.md                  # This file

---

## Key Features

### Authentication & Authorization
- **Role-Based Access**: Users and Providers with different permissions
- **Single Login Endpoint**: Returns role for frontend redirect
- **JWT Authentication**: Secure token-based auth
- **Profile Management**: Update profile and photos

### Provider Management
- **Admin Creates Providers**: Controlled provider onboarding
- **Provider Dashboard**: Manage bookings and availability
- **Availability Calendar**: Set available time slots
- **Multi-Language Support**: English and Nepali content

### Booking System
- **Conflict Prevention**: No double-booking same time slot
- **Status Workflow**: Pending → Confirmed → Completed/Cancelled
- **Email Notifications**: Automatic notifications for all parties
- **Booking History**: Track past and upcoming bookings

### API Features
- **RESTful Design**: Standard REST principles
- **Pagination**: Built-in for large datasets
- **Filtering**: Advanced filtering and search
- **CORS Enabled**: Ready for frontend integration

---

## Production Deployment

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-very-long-random-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=meropanditlama
DB_USER=dbuser
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Email (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_specific_password

FRONTEND_URL=https://yourdomain.com
```

### Static Files Collection
```bash
python manage.py collectstatic --no-input
```

### Database Migration (PostgreSQL)

Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

Update `api/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'meropanditlama',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Key Features

### Authentication & Authorization
- **Role-Based Access**: Users and Providers with different permissions
- **Single Login Endpoint**: Returns role for frontend redirect
- **JWT Authentication**: Secure token-based auth
- **Profile Management**: Update profile and photos

### Provider Management
- **Admin Creates Providers**: Controlled provider onboarding
- **Provider Dashboard**: Manage bookings and availability
- **Availability Calendar**: Set available time slots
- **Multi-Language Support**: English and Nepali content

### Booking System
- **Conflict Prevention**: No double-booking same time slot
- **Status Workflow**: Pending → Confirmed → Completed/Cancelled
- **Email Notifications**: Automatic notifications for all parties
- **Booking History**: Track past and upcoming bookings

### API Features
- **RESTful Design**: Standard REST principles
- **Pagination**: Built-in for large datasets
- **Filtering**: Advanced filtering and search
- **CORS Enabled**: Ready for frontend integration

---

## Production Deployment

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-very-long-random-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=meropanditlama
DB_USER=dbuser
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Email (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_specific_password

FRONTEND_URL=https://yourdomain.com
```

### Static Files Collection
```bash
python manage.py collectstatic --no-input
```

### Database Migration (PostgreSQL)

Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

Update `api/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'meropanditlama',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Troubleshooting

### Common Issues

#### 1. Migration Errors
```bash
# Delete migrations and recreate
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
```

#### 2. Static Files Not Loading
```bash
python manage.py collectstatic --clear
```

#### 3. CORS Issues
In `api/settings.py`, ensure:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
```

#### 4. Media Files Not Serving
Ensure in `api/urls.py`:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### 5. Email Not Sending
For development, emails print to console. Check terminal output.

For production SMTP issues:
- Use app-specific passwords for Gmail
- Enable "Less secure app access" (not recommended)
- Or use services like SendGrid, Mailgun

---

## Support & Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **JWT Authentication**: https://django-rest-framework-simplejwt.readthedocs.io/

---

## Next Steps

1. ✅ Complete setup steps above
2. ✅ Test all API endpoints with cURL or Postman
3. ✅ Create test accounts (users and providers)
4. ✅ Integrate with Vue.js frontend
5. ✅ Implement role-based routing in frontend
6. ✅ Add Google OAuth (optional)
7. ✅ Deploy to production

This API provides a complete backend solution for MeroPanditLama with role-based authentication, provider management, booking system, and email notifications. Ready for frontend integration!