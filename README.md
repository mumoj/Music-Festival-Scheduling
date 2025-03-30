# Kenya Music Festival Management System

A Django-based web application for managing performances, venues, and scheduling for the Kenya Music Festival.

## Overview

This system facilitates the management of various aspects of music festivals, including:

- User account management with different roles (Teachers, Adjudicators, Performers, Sponsors, etc.)
- Institution management and registration
- Performance tracking and scheduling
- Automatic timetable generation for events
- PDF export of schedules

## Project Structure

The project consists of two main Django apps:

### 1. Accounts App

Handles user management with custom user model supporting different roles:

- **Teachers**: Responsible for performances in institutions
- **Adjudicators**: Judges of performances
- **Independent Performers**: Self-paying performers
- **Dependent Performers**: School-going performers dependent on teachers
- **Sponsors**: Financial sponsors for underage performers
- **Heads of Institutions**: Institutional administrators

### 2. Performances App

Manages festival performances and scheduling with models for:

- **Institutions**: Schools or organizations participating in the festival
- **Classes**: Performance categories (songs, dances, etc.)
- **Performances**: Individual or group performances
- **Events**: Festival events with venues and levels (zonal, sub-county, county, etc.)
- **Theaters**: Venues within events where performances take place
- **Localities**: Geographical divisions (zones, sub-counties, counties, regions)

## Key Features

- **Custom User Authentication**: Email-based authentication with role-based permissions
- **Automatic Scheduling Algorithm**: Creates optimized performance schedules based on venues, time constraints
- **REST API**: Frontend-backend communication via RESTful endpoints
- **PDF Generation**: Export of performance timetables to PDF
- **Role-Based Access Control**: Different permissions based on user roles

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: Vue.js
- **Database**: PostgreSQL
- **Authentication**: Django-allauth, Django REST Auth
- **PDF Generation**: pdfkit, wkhtmltopdf

## Setup and Installation

### Prerequisites

- Python 3.6+
- PostgreSQL
- Node.js and npm (for frontend)
- wkhtmltopdf (for PDF generation)

### Backend Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd kenya-music-festival
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure PostgreSQL database in `config/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '',
       }
   }
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run serve
   ```

## API Endpoints

### Accounts

- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/teacher/<id>/details/` - Teacher profile management
- `/accounts/sponsor/<id>/details/` - Sponsor profile management
- `/accounts/dependent_performer/<id>/details/` - Dependent performer profile management
- `/accounts/independent_performer/<id>/details/` - Independent performer profile management

### Performances

- `/performances/register-institution/<id>` - Institution registration
- `/performances/schedule-performances/<event_id>` - Generate schedule for an event

## User Roles and Permissions

- **Head of Institution**: Register and manage institutions
- **Teacher**: Register and manage performances for dependent performers
- **Adjudicator**: Judge performances
- **Independent Performer**: Register and manage own performances
- **Dependent Performer**: Participate in performances managed by teachers
- **Sponsor**: Financially support dependent performers

## Development

### Testing

Run tests with:
```
python manage.py test
```

The project uses `model_bakery` for test fixtures.

### Code Organization

- `accounts/`: User models, authentication, and profile management
- `performances/`: Festival, venue, and scheduling management
- `config/`: Project settings and configuration
- `frontend/`: Vue.js frontend application
