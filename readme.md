# TicketFast

TicketFast is a full-stack ticketing application for browsing live events, checking ticket availability, and creating and managing bookings.

It uses a Django REST Framework backend, a React + Vite frontend, JWT authentication, PostgreSQL, and separate cloud deployments for the API and user interface.

## Live deployment

| Service | URL |
|---|---|
| React frontend | https://ticketing-frontend.snowdoncoder.workers.dev |
| Django REST API | https://ticketfast-api-ea43d8acd123.herokuapp.com |
| API health check | https://ticketfast-api-ea43d8acd123.herokuapp.com/api/health/ |
| Events API | https://ticketfast-api-ea43d8acd123.herokuapp.com/api/events/ |

## Tech stack

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- django-filter
- django-cors-headers
- Gunicorn
- WhiteNoise
- pytest

### Frontend

- React
- Vite
- JavaScript
- Shared API request client
- Centralised API error handling

### Infrastructure

- GitHub Actions for backend CI/CD
- Heroku for Django API hosting and PostgreSQL
- Cloudflare Workers for React static hosting
- Environment-based configuration for local and production environments

## Features

### Events

- Public listing of published, upcoming events
- Event detail endpoint including ticket types
- Search across event title, description, venue name, and city
- Filtering by city and venue
- Ordering by event start time
- Ticket availability and maximum-per-booking rules

### Bookings

- Authenticated booking creation
- Booking references for customer-friendly retrieval
- Booking detail and cancellation endpoints
- Transactional booking service to reduce the risk of overselling
- Cancelled bookings return tickets to availability
- Users can only access their own bookings

### Authentication

- User registration
- JWT access and refresh tokens
- Token refresh endpoint
- Authenticated current-user endpoint
- Protected booking endpoints

## API overview

All API routes are namespaced under `/api/`.

### Health

```http
GET /api/health/
```

Returns a simple health response.

### Events

```http
GET /api/events/
```

Returns published, upcoming events.

Supported query parameters:

| Parameter | Example | Description |
|---|---|---|
| `search` | `?search=manchester` | Searches event title, description, venue name, and venue city |
| `city` | `?city=Manchester` | Filters events by venue city |
| `venue` | `?venue=manchester-academy` | Filters events by venue slug |
| `ordering` | `?ordering=starts_at` | Orders events by start time |
| `ordering` | `?ordering=-starts_at` | Orders events by newest start time first |

```http
GET /api/events/<id>/
```

Returns a single event, including its available ticket types.

### Authentication

```http
POST /api/auth/register/
```

Request:

```json
{
  "username": "demo_user",
  "email": "demo@example.com",
  "password": "StrongPassword123!"
}
```

```http
POST /api/auth/token/
```

Request:

```json
{
  "username": "demo_user",
  "password": "StrongPassword123!"
}
```

Response:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

Use the access token for protected requests:

```http
Authorization: Bearer <access-token>
```

```http
POST /api/auth/token/refresh/
```

Request:

```json
{
  "refresh": "<refresh-token>"
}
```

```http
GET /api/auth/me/
```

Returns the authenticated user.

### Bookings

All booking endpoints require a JWT access token.

```http
GET /api/bookings/
```

Returns bookings belonging to the authenticated user.

```http
POST /api/bookings/
```

Request:

```json
{
  "ticket_type_id": 1,
  "quantity": 2
}
```

The API validates that:

- The ticket type exists.
- The quantity is at least 1.
- The quantity does not exceed `max_per_booking`.
- Enough tickets remain available.
- The booking is created transactionally.

```http
GET /api/bookings/<reference>/
```

Returns a single booking using its unique reference.

```http
POST /api/bookings/<reference>/cancel/
```

Cancels the authenticated user’s booking and returns its tickets to availability.

## Business rules

- Only published, upcoming events are publicly listed.
- A booking must contain at least one ticket.
- A booking cannot exceed the ticket type’s `max_per_booking` value.
- A booking cannot exceed remaining ticket availability.
- Bookings are created through a transactional service to reduce overselling risk.
- Cancelling a booking returns its tickets to availability.
- Users can only view and cancel their own bookings.

## Project structure

```text
accounts/
    User model and authentication-related logic

api/
    API serializers, views, and URL routing

config/
    Django project settings and root URL configuration

tickets/
    Venue, Event, TicketType, Booking, and BookingItem models
    Booking service logic
    Demo data management command
    Tests

ticketing-frontend/
    React + Vite frontend
```

## Local development

### Prerequisites

- Python 3.12+
- PostgreSQL
- Node.js

### Backend setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

The local API is available at:

```text
http://127.0.0.1:8000
```

### Frontend setup

```bash
cd ticketing-frontend
npm install
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

Create a `.env` file inside `ticketing-frontend`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Environment variables

### Backend

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DEBUG` | Enables Django debug mode |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of permitted hosts |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of permitted frontend origins |
| `DATABASE_URL` | Heroku PostgreSQL connection URL |
| `DB_NAME` | Local PostgreSQL database name |
| `DB_USER` | Local PostgreSQL user |
| `DB_PASSWORD` | Local PostgreSQL password |
| `DB_HOST` | Local PostgreSQL host |
| `DB_PORT` | Local PostgreSQL port |

The backend uses `DATABASE_URL` when it is present, such as on Heroku. Otherwise, it falls back to the individual `DB_*` variables for local PostgreSQL development.

### Frontend

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Base URL of the Django API |

## Testing

Run the backend test suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest api/tests/test_booking_api.py
```

## Deployment

### Backend

The Django API is deployed to Heroku through GitHub Actions.

On every relevant push to `main`, GitHub Actions:

1. Installs Python dependencies.
2. Runs Django system checks.
3. Pushes the repository to Heroku.
4. Heroku applies database migrations through the release process.
5. Heroku starts the API using Gunicorn.

The `Procfile` contains:

```text
release: python manage.py migrate
web: gunicorn config.wsgi --log-file -
```

### Frontend

The React frontend is deployed to Cloudflare Workers.

Cloudflare:

1. Connects to the GitHub repository.
2. Changes into `ticketing-frontend`.
3. Installs npm dependencies.
4. Runs `npm run build`.
5. Publishes the generated `dist` directory.

The frontend is configured with:

```env
VITE_API_BASE_URL=[https://ticketfast-api-ea43d8acd123.herokuapp.com](https://ticketfast-api-ea43d8acd123.herokuapp.com)
```

## Demo data

To create demo venues, events, and ticket types:

```bash
python manage.py seed_demo_data
```

On Heroku:

```bash
heroku run python manage.py seed_demo_data -a ticketfast-api-ea43d8acd123
```

The command is idempotent, so it can safely be run more than once.

## Postman

A Postman collection is available for testing the deployed API:

```text
ticketfast-live.postman_collection.json
```

Import it into Postman, set the `username` and `password` collection variables, then run **Auth → Login** before testing protected booking endpoints.

## License

This project was created for assessment and development purposes.