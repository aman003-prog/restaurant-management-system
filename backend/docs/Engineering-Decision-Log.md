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

---

## 2026-08-04

### Completed
- Implemented Category CRUD API using DRF Generic Views.
- Created `CategorySerializer` using `ModelSerializer`.
- Configured `slug` and `id` as read-only fields in the serializer.
- Implemented automatic slug generation using `slugify()` inside the model's `save()` method.
- Configured Category URLs using slug-based lookup.
- Added filtering support using `DjangoFilterBackend`.
- Added search functionality using `SearchFilter`.
- Added ordering functionality using `OrderingFilter`.
- Implemented filtering by `is_active`.
- Added search support for `title` and `description`.
- Added ordering support for `title` and `created_at`.
- Created custom permission architecture in `apps/core/permissions.py`.
- Implemented reusable `BaseGroupPermission`.
- Created `IsManager`, `IsDeliveryCrew`, and `IsKitchenStaff` permissions.
- Created role constants in `core/constants.py`.
- Created Django Groups (`Manager`, `Delivery Crew`, `Kitchen Staff`) through Django Admin.
- Created test users for Manager and Customer roles.
- Replaced `IsAdminUser` with custom `IsManager` permission for Category write operations.
- Tested Category API endpoints for public read access and manager-only write access.

### Problems Faced
- Understanding how to design reusable permission classes using inheritance.
- Confusion about whether to use helper functions or a base permission class.
- Understanding when to use `get_permissions()` versus `permission_classes`.
- Confusion about designing `RoleOrReadOnly` permissions without duplicating logic.
- Understanding how child permission classes inherit behavior from a base permission class.
- Deciding where shared permission logic should be placed (`permissions.py` vs `helpers.py` vs `utils.py`).
- Understanding how to organize reusable constants for role names.

### Learned
- DRF permission classes can be designed using inheritance to eliminate duplicated authorization logic.
- A base permission class (`BaseGroupPermission`) provides a scalable architecture for role-based authorization.
- Class attributes (e.g., `group_name`) allow child permission classes to customize shared behavior.
- `superuser` checks should be handled centrally inside the base permission class.
- Django Groups represent business roles, while Django Model Permissions represent specific capabilities.
- `SAFE_METHODS` (`GET`, `HEAD`, `OPTIONS`) are preferred over checking only `"GET"` for read-only access.
- `SearchFilter`, `OrderingFilter`, and `DjangoFilterBackend` can be combined to provide flexible API querying.
- Slug generation belongs in the model rather than the serializer or view because the model is the single source of truth.
- Using constants for group names improves maintainability and avoids hardcoded strings throughout the project.
- Avoid premature abstraction (YAGNI); introduce reusable permission classes only when multiple endpoints require the same behavior.