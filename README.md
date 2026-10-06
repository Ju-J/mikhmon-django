# Mikhmon Django

A Django-based MikroTik Hotspot management server inspired by Mikhmon.

## Features
- RouterOS API integration
- Router device management
- Hotspot user management
- Voucher generation
- Active session monitoring
- REST API endpoints

## Quick start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Notes
This project is a strong starting point and is designed to be extended for production deployment, including authentication, advanced reporting, and integration with real MikroTik RouterOS environments.
