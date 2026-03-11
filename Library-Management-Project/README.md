# 📚 Library Management System

A comprehensive web-based Library Management System built with Django and MySQL, designed to streamline library operations in educational institutions. The system provides a user-friendly interface for both administrators and students to manage library resources efficiently.

## ✨ Key Features

### 👨‍💼 Admin Dashboard
- **Book Management**
  - Add new books with details (Title, Author, Subject, Quantity)
  - View and search all books in the library
  - Update book information and availability
  - Remove books from the system

- **Student Management**
  - Register new students with personal details
  - View and search student records
  - Manage student accounts and access
  - Track student activity and history

- **Issue/Return System**
  - Process book issues to students
  - Handle book returns and manage due dates
  - View all active transactions
  - Generate reports and analytics

### 👨‍🎓 Student Portal
- **Book Operations**
  - Browse available books with search functionality
  - View book details and availability status
  - Request book issues
  - Check due dates for borrowed books
  - View borrowing history

- **User Account**
  - Secure login/logout functionality
  - View personal information
  - Track current and past book issues
  - Update profile information

## 🛠️ Technical Stack

### Backend
- **Framework**: Django 4.2
- **Database**: MySQL 8.0+
- **Authentication**: Django's built-in authentication system
- **API**: Django REST Framework (for future API development)

### Frontend
- **HTML5**
- **CSS3** with Bootstrap 5
- **JavaScript**
- **jQuery** (for AJAX and DOM manipulation)

### Development Tools
- Version Control: Git
- Package Manager: pip
- Virtual Environment: venv
- IDE: VS Code (recommended)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)
- Git (for version control)

### Installation Guide

#### 1. Clone the Repository
```bash
git clone https://github.com/Sagargupta028/Library-Management-Project.git
cd Library-Management-Project
```

#### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Database Configuration
1. Create a new MySQL database:
   ```sql
   CREATE DATABASE LibraryDjango CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```
   Example `.env` file:
   ```env
   # Django Settings
   SECRET_KEY=your-secure-secret-key-here
   DEBUG=True
   
   # Database Settings
   DB_NAME=LibraryDjango
   DB_USER=your_db_username
   DB_PASSWORD=your_secure_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

#### 5. Run Migrations
```bash
python manage.py migrate
```

#### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

#### 7. Load Initial Data (Optional)
```bash
python manage.py loaddata sample_data.json
```

#### 8. Start Development Server
```bash
python manage.py runserver
```

## 🌐 Access the Application

- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Student Login**: http://127.0.0.1:8000/login/
- **Default Admin Credentials** (if using sample data):
  - Username: admin
  - Password: admin123

## 🧪 Testing

Run the test suite with:
```bash
python manage.py test
```

## 🔧 Project Structure

```
Library-Management-Project/
├── library/                  # Main application
│   ├── migrations/          # Database migrations
│   ├── static/              # Static files (CSS, JS, images)
│   │   ├── css/            # Stylesheets
│   │   ├── js/             # JavaScript files
│   │   └── img/            # Image assets
│   │
│   ├── templates/           # HTML templates
│   │   ├── admin/          # Admin-specific templates
│   │   ├── student/        # Student portal templates
│   │   └── base.html       # Base template
│   │
│   ├── admin.py            # Admin site configuration
│   ├── models.py           # Database models
│   ├── urls.py            # Application URL routing
│   ├── views.py           # View functions
│   └── forms.py           # Form definitions
│
├── library_project/        # Project configuration
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
│
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```



