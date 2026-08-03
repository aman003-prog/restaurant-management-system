# User APIs

Base URL

```
/api/
```

---

## User Profile

### GET `/users/me/`

Returns the authenticated user's profile.

Example Response

```json
{
    "username": "aman",
    "first_name": "Aman",
    "last_name": "Gupta",
    "email": "aman@example.com",
    "phone_number": "9876543210",
    "date_of_birth": "2006-04-01",
    "profile_image": null,
    "is_active": true
}
```

---

### PUT `/users/me/`

Updates the complete user profile.

Request Body

```json
{
    "first_name": "Aman",
    "last_name": "Gupta",
    "email": "aman@example.com",
    "phone_number": "9876543210",
    "date_of_birth": "2006-04-01",
    "profile_image": null
}
```

---

### PATCH `/users/me/`

Partially updates the authenticated user's profile.

Example

```json
{
    "phone_number": "9999999999"
}
```

---

### DELETE `/users/me/`

Currently disabled.

Returns

```json
{
    "detail": "Account deletion is temporarily disabled. This feature will require password confirmation and/or email verification."
}
```

---

## Addresses

### GET `/users/addresses/`

Returns all addresses belonging to the authenticated user.

Example Response

```json
[
    {
        "label": "Home",
        "address": "Street 123",
        "city": "Delhi",
        "state": "Delhi",
        "country": "India",
        "postal_code": "110001",
        "is_default": true
    }
]
```

---

### POST `/users/addresses/`

Creates a new address.

Request Body

```json
{
    "label": "Home",
    "address": "Street 123",
    "city": "Delhi",
    "state": "Delhi",
    "country": "India",
    "postal_code": "110001",
    "is_default": true
}
```

---

## Single Address

### GET `/users/addresses/<id>/`

Returns a single address if it belongs to the authenticated user.

---

### PUT `/users/addresses/<id>/`

Updates the complete address.

---

### PATCH `/users/addresses/<id>/`

Partially updates the address.

Example

```json
{
    "city": "Noida"
}
```

---

### DELETE `/users/addresses/<id>/`

Currently disabled.

Returns

```json
{
    "detail": "Address deletion is temporarily disabled. This feature will require password confirmation and/or email verification."
}
```