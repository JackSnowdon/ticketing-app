# Ticketing API Reference

Base URL during local development:

```text
http://127.0.0.1:8000
```

All responses are JSON.

Public event endpoints do not require authentication. Booking endpoints require a valid JWT access token.

## Authentication

### Obtain tokens

```http
POST /api/token/
```

Request:

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

Success response:

```text
200 OK
```

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

Use the access token for protected endpoints:

```http
Authorization: Bearer <access-token>
```

### Refresh token

```http
POST /api/token/refresh/
```

Request:

```json
{
  "refresh": "<refresh-token>"
}
```

Success response:

```text
200 OK
```

```json
{
  "access": "<new-access-token>"
}
```

## Events

### List events

```http
GET /tickets/events/
```

Returns a paginated list of published, upcoming events.

Query parameters:

| Parameter | Type | Example | Description |
|---|---|---|---|
| `search` | string | `?search=wolverhampton` | Searches event title, description, venue name, and venue city |
| `ordering` | string | `?ordering=starts_at` | Orders results ascending |
| `ordering` | string | `?ordering=-starts_at` | Orders results descending |
| `city` | string | `?city=Wolverhampton` | Filters by venue city, case-insensitive |
| `venue` | string | `?venue=kks-steel-mill` | Filters by venue slug, case-insensitive |
| `page` | integer | `?page=2` | Returns a specific page |

Allowed ordering fields:

```text
starts_at
title
```

Default ordering:

```text
starts_at
```

Example:

```http
GET /tickets/events/?city=Wolverhampton&search=gig&ordering=-starts_at
```

Success response:

```text
200 OK
```

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Test Event",
      "description": "A test event",
      "venue": {
        "id": 1,
        "name": "KK's Steel Mill",
        "city": "Wolverhampton",
        "slug": "kks-steel-mill"
      },
      "starts_at": "2026-11-20T19:30:00Z",
      "doors_open_at": "2026-11-20T18:30:00Z",
      "ticket_types": [
        {
          "id": 1,
          "name": "Standard",
          "price": "25.00",
          "quantity_available": 10,
          "max_per_booking": 4
        }
      ]
    }
  ]
}
```

### Event detail

```http
GET /tickets/events/<event_id>/
```

Returns one published event.

Success response:

```text
200 OK
```

Errors:

| Status | Meaning |
|---|---|
| `404 Not Found` | Event does not exist or is not published |

## Bookings

All booking endpoints require authentication.

### Create booking

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

Success response:

```text
201 Created
```

```json
{
  "id": 12,
  "reference": "A1B2C3D4E5F6",
  "status": "pending",
  "created_at": "2026-11-02T16:30:00Z",
  "updated_at": "2026-11-02T16:30:00Z",
  "items": [
    {
      "id": 18,
      "ticket_type": 1,
      "ticket_type_name": "Standard",
      "event_title": "Test Event",
      "quantity": 2,
      "unit_price": "25.00",
      "line_total": "50.00"
    }
  ],
  "total": "50.00"
}
```

Validation rules:

| Rule | Error response |
|---|---|
| Quantity must be at least 1 | `400 Bad Request` |
| Ticket type must exist | `400 Bad Request` |
| Quantity cannot exceed `max_per_booking` | `400 Bad Request` |
| Ticket availability must be sufficient | `400 Bad Request` |
| Event must be published | `400 Bad Request` |
| Event must not have started | `400 Bad Request` |

Example validation error:

```text
400 Bad Request
```

```json
{
  "quantity": [
    "You can book a maximum of 4 Standard tickets per booking."
  ]
}
```

Example availability error:

```text
400 Bad Request
```

```json
{
  "detail": "Not enough tickets are available for this booking."
}
```

### List bookings

```http
GET /api/bookings/
```

Returns bookings belonging to the authenticated user only.

Success response:

```text
200 OK
```

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 12,
      "reference": "A1B2C3D4E5F6",
      "status": "pending",
      "created_at": "2026-11-02T16:30:00Z",
      "updated_at": "2026-11-02T16:30:00Z",
      "items": [
        {
          "id": 18,
          "ticket_type": 1,
          "ticket_type_name": "Standard",
          "event_title": "Test Event",
          "quantity": 2,
          "unit_price": "25.00",
          "line_total": "50.00"
        }
      ],
      "total": "50.00"
    }
  ]
}
```

### Booking detail

```http
GET /api/bookings/<booking_reference>/
```

Returns a single booking belonging to the authenticated user.

Success response:

```text
200 OK
```

Errors:

| Status | Meaning |
|---|---|
| `401 Unauthorized` | No valid access token was supplied |
| `404 Not Found` | Booking does not exist or belongs to another user |

### Cancel booking

```http
POST /api/bookings/<booking_reference>/cancel/
```

Cancels a pending booking and returns its tickets to availability.

Success response:

```text
200 OK
```

```json
{
  "id": 12,
  "reference": "A1B2C3D4E5F6",
  "status": "cancelled",
  "created_at": "2026-11-02T16:30:00Z",
  "updated_at": "2026-11-02T16:35:00Z",
  "items": [
    {
      "id": 18,
      "ticket_type": 1,
      "ticket_type_name": "Standard",
      "event_title": "Test Event",
      "quantity": 2,
      "unit_price": "25.00",
      "line_total": "50.00"
    }
  ],
  "total": "50.00"
}
```

Errors:

| Status | Meaning |
|---|---|
| `400 Bad Request` | Booking is already cancelled or confirmed |
| `401 Unauthorized` | No valid access token was supplied |
| `404 Not Found` | Booking does not exist or belongs to another user |

## Health check

```http
GET /api/health/
```

Used to confirm that the API is running.

## Status code summary

| Status | Meaning |
|---|---|
| `200 OK` | Successful read or update |
| `201 Created` | Booking created successfully |
| `400 Bad Request` | Invalid input or business-rule failure |
| `401 Unauthorized` | Missing or invalid authentication credentials |
| `403 Forbidden` | Authenticated user is not permitted to perform the action |
| `404 Not Found` | Requested resource does not exist or is not visible to the user |
| `429 Too Many Requests` | Rate limit exceeded |

## React integration notes

For local development, React should call:

```text
http://127.0.0.1:8000
```

Django allows CORS requests from:

```text
http://localhost:5173
http://127.0.0.1:5173
```

For protected booking requests, React should store the JWT access token in memory and attach:

```http
Authorization: Bearer <access-token>
```

When the access token expires, call:

```http
POST /api/token/refresh/
```

For field-level validation errors, React can display messages beside the relevant input:

```json
{
  "quantity": [
    "You can book a maximum of 4 Standard tickets per booking."
  ]
}
```

For service-level business errors, React can display the `detail` message:

```json
{
  "detail": "Not enough tickets are available for this booking."
}
```