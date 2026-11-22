# Meridian – E-commerce System

## 1. Project Overview

Meridian is a Django-based e-commerce web application developed as an academic project. It provides a central platform where users can register, browse products, search for items, manage a shopping cart, save delivery addresses, place orders and view their order history.

## 2. Features

- User registration and login
- Email OTP verification workflow
- Product browsing and search
- Product categories and sorting
- Shopping cart management
- Delivery address management
- Checkout and simulated payment
- Order confirmation and order history
- Order cancellation
- Django administration panel for managing products, categories, users, orders and payments

## 3. Technology Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Development environment:** Visual Studio Code
- **Version control:** Git and GitHub

## 4. Project Structure

```text
Meridian_Ecommerce_Project/
├── diagrams/
├── meridian/
├── static/
│   └── css/
├── store/
├── templates/
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/anirudhap2006/Meridian-Ecommerce-System-Copy.git
cd Meridian-Ecommerce-System-Copy
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Apply database migrations

```bash
python manage.py migrate
```

### Step 6: Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator username and password.

### Step 7: Run the application

```bash
python manage.py runserver
```

Open the following address in your browser:

http://127.0.0.1:8000/

## 6. Administration Panel

The Django administration panel is available at:

http://127.0.0.1:8000/admin/

Log in using the administrator account created during setup. The administrator can manage products, categories, users, addresses, orders and payment records.

## 7. Testing

Run the automated test suite using:

```bash
python manage.py test
```

The project includes automated tests for key application functionality.

## 8. Payment and Verification Notes

Meridian is an academic demonstration application. Payments are simulated; no real money is charged. The verification workflow is intended for demonstration and should not be treated as a production email or OTP delivery service.

## 9. Project Purpose

The project demonstrates the application of software development fundamentals, database management, user authentication, web application architecture, shopping cart functionality, order processing and software testing.

---

**Project Name:** Meridian  
**Project Type:** Academic E-commerce Web Application  
**Repository:** https://github.com/anirudhap2006/Meridian-Ecommerce-System-Copy
