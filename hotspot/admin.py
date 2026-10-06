# Mikhmon Django

A Django-based MikroTik Hotspot Manager inspired by the Mikhmon workflow.

## Features
- Router device management
- Hotspot profile configuration
- Hotspot user CRUD and status toggling
- Voucher generation and tracking
- Active session monitoring
- REST API for clients and integrations
- Modern Bootstrap dashboard

## Tech stack
- Django 5
- Django REST Framework
- SQLite by default
- RouterOS API via `routeros-api`

## Quick start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then browse to:
- http://127.0.0.1:8000/

## Notes
This project is designed as a practical foundation for MikroTik hotspot management systems. To connect to real RouterOS devices, configure your router credentials in the Django admin or through the router form.

## Important
RouterOS API commands may vary slightly depending on your MikroTik device model and RouterOS version. Test all commands against your target environment before production deployment.
