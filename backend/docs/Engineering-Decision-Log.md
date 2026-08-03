# Development Log

## 2026-08-02

### Completed
- Created project structure.
- Initialized Git repository.
- Created `core` app.
- Added `TimeStampedModel`.
- Created custom `User` model.
- Created `Address` model.
- Added model constraints.
- Configured PostgreSQL.
- Ran migrations successfully.
- Created Django superuser.
- Pushed initial project to GitHub.

### Problems Faced
- Module import error (`ModuleNotFoundError`).
- Nested Git repository issue.
- Migration history inconsistency.
- Missing migration file.

### Learned
- Why to use a custom `User` model.
- Abstract models (`TimeStampedModel`).
- `related_name`.
- `UniqueConstraint`.
- Conditional constraints using `Q`.
- Reading Django tracebacks.
- Git repositories should not be nested.

---

## 2026-08-03

### Completed
- Created `UserProfileSerializer`.
- Created `AddressSerializer`.
- Implemented User Profile API.
- Implemented Address List & Create API.
- Implemented Single Address API.
- Added authentication using `IsAuthenticated`.
- Filtered address queries by authenticated user.
- Implemented automatic default address handling during address creation.
- Temporarily disabled User deletion.
- Temporarily disabled Address deletion.
- Tested all User Profile endpoints.
- Tested Address List, Create, Retrieve, Update endpoints.
- Verified address ownership protection.

### Problems Faced
- Confusion between `get_queryset()` and `get_object()`.
- Understanding when DRF automatically fetches objects.
- Confusion about how Generic Views work internally.
- Confusion regarding PostgreSQL auto-increment IDs after deleted records.

### Learned
- Difference between `RetrieveAPIView`, `ListAPIView`, and other Generic Views.
- Purpose of `get_queryset()`.
- Purpose of `get_object()`.
- Purpose of `perform_create()`.
- How DRF automatically handles GET, POST, PUT, PATCH, and DELETE.
- How authentication identifies the current user using `request.user`.
- Primary Keys are unique identifiers, not row numbers.
- PostgreSQL does not reuse deleted primary key values.