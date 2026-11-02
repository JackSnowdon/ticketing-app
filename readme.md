# Ticketing API

A Django REST Framework API for browsing published events, viewing ticket types, and creating and managing bookings.

The project is designed to support a React frontend and uses JWT authentication for customer actions such as creating bookings.

## Features

- Public event listing and detail endpoints
- Event search, ordering, city filtering, and venue filtering
- Ticket types with availability and per-booking limits
- Authenticated booking creation
- Booking retrieval and cancellation
- Transactional booking service to reduce the risk of overselling
- JWT authentication
- CORS configuration for local React development
- PostgreSQL support
- Test suite using pytest

## Tech stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- django-filter
- Simple JWT
- django-cors-headers
- pytest

## Project structure

```text
api/
    serializers/
    views/
    tests/
    urls.py

config/
    settings.py
    urls.py

tickets/
    models.py
    services/
    tests/
    admin.py
```

## Local setup

### Prerequisites

- Python 3.12+
- PostgreSQL
- Node.js, if running the React frontend locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Then update the values for your local PostgreSQL database.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Load demo data

```bash
python manage.py seed_demo_data
```

This creates public demo venues, upcoming events, and ticket types.

The command is idempotent, so it can safely be run more than once.

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Environment variables

| Variable | Purpose | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | A long random string |
| `DEBUG` | Enables Django debug mode | `True` locally, `False` in production |
| `DB_NAME` | PostgreSQL database name | `ticketing` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | Local database password |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated allowed frontend origins | `http://localhost:5173` |

Never commit the real `.env` file.

## Running tests

```bash
pytest
```

Run a specific test file:

```bash
pytest api/tests/test_booking_api.py
```

## API overview

### Public events

```http
GET /tickets/events/
```

Returns published, upcoming events.

Supported query parameters:

| Parameter | Example | Description |
|---|---|---|
| `search` | `?search=wolverhampton` | Searches event title, description, venue name, and venue city |
| `ordering` | `?ordering=starts_at` | Orders results ascending |
| `ordering` | `?ordering=-starts_at` | Orders results descending |
| `city` | `?city=Wolverhampton` | Filters by venue city |
| `venue` | `?venue=kks-steel-mill` | Filters by venue slug |

### Event detail

```http
GET /tickets/events/<id>/
```

Returns a single published event, including its ticket types.

### Authentication

```http
POST /api/auth/token/
```

Request:

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

Response:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

Use the access token in protected requests:

```http
Authorization: Bearer <access-token>
```

### Create booking

```http
POST /api/bookings/
```

Requires authentication.

Request:

```json
{
  "ticket_type_id": 1,
  "quantity": 2
}
```

Success response:

```text
201 Created
```

Validation and availability errors return:

```text
400 Bad Request
```

### List bookings

```http
GET /api/bookings/
```

Returns bookings belonging to the authenticated user.

### Booking detail

```http
GET /api/bookings/<reference>/
```

### Cancel booking

```http
POST /api/bookings/<reference>/cancel/
```

## Business rules

- Only published, upcoming events are publicly listed.
- Booking quantity must be at least 1.
- A booking cannot exceed the ticket type’s `max_per_booking`.
- A booking cannot exceed remaining ticket availability.
- Bookings are created through a transactional service.
- Cancelling a pending booking returns its tickets to availability.
- Users can only view and cancel their own bookings.

## Deployment notes

The project is configured to read sensitive settings from environment variables.

For a future Heroku deployment:

- Set `DEBUG=False`
- Set a strong `DJANGO_SECRET_KEY`
- Set `DJANGO_ALLOWED_HOSTS` to the Heroku domain
- Set `CORS_ALLOWED_ORIGINS` to the deployed React domain
- Provide PostgreSQL connection settings through environment variables
- Run migrations during deployment
- Run `python manage.py collectstatic` if serving Django Admin

## License

This project is for assessment and development purposes.