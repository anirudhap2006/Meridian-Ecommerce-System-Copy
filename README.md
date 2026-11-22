# Meridian — E-commerce Shopping and Order Management System

Meridian is an academic Django prototype. Customers can register with email OTP verification, browse/search products, manage a cart and delivery addresses, simulate checkout/payment, and view/cancel orders. Administrators manage products, categories, stock and orders through Django Admin.

## Stack
Python, Django 5.2, SQLite, HTML, CSS.

## Windows / VS Code setup
1. Extract the ZIP and open `Meridian_Ecommerce_Project` in VS Code.
2. Terminal → New Terminal.
3. `python -m venv venv`
4. `.env\Scripts\Activate.ps1`
5. `python -m pip install -r requirements.txt`
6. `python manage.py makemigrations store`
7. `python manage.py migrate`
8. `python manage.py createsuperuser`
9. `python manage.py runserver`
10. Open http://127.0.0.1:8000/

## Email OTP
In local development Django prints the OTP email to the VS Code terminal using the console email backend. For real email delivery configure `DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` and `DEFAULT_FROM_EMAIL` as environment variables. Never commit email credentials.

## Add sample catalogue
Visit `/admin/`, create Categories (e.g. Electronics, Books, Home), then Products with unique slug, description, price, stock and optional image URL.

## Payments
Card/UPI methods and success/failure are simulations only. No real money or payment credentials are processed.

## Tests
Run `python manage.py test`. The starter suite covers product search, login protection, cart addition, successful checkout/stock deduction and failed-payment stock preservation.

## Limitations
Single-store catalogue managed by administrators; seller onboarding, real payment gateway, live shipping, and production email delivery are not included by default. SQLite is for local academic demonstration.
