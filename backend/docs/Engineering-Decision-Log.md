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
- Implemented Category CRUD API using DRF generic views.
- Created `CategorySerializer` with read-only `id` and `slug` fields.
- Implemented automatic slug generation in the model's `save()` method.
- Added filtering, search, and ordering support (`DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`).
- Built custom permission architecture in `apps/core/permissions.py`.
- Created reusable `BaseGroupPermission` class.
- Created `IsManager`, `IsDeliveryCrew`, and `IsKitchenStaff` permissions.
- Configured role constants in `core/constants.py`.
- Created Django groups (`Manager`, `Delivery Crew`, `Kitchen Staff`) and test users.
- Verified public read access and manager-only write access across endpoints.

### Problems Faced
- Designing reusable permission classes using inheritance.
- Understanding when to use `get_permissions()` vs `permission_classes`.
- Structuring role-based read/write access without duplicating logic.
- Deciding where to place shared authorization logic.

### Learned
- Reusable DRF permissions using base class inheritance (`BaseGroupPermission`).
- Centralizing `superuser` checks inside the base permission class.
- Using `SAFE_METHODS` (`GET`, `HEAD`, `OPTIONS`) for read-only access checks.
- Combining filter backends for flexible querying.
- Keeping slug generation in the model as the single source of truth.
- Storing group names as central constants to avoid hardcoded strings.

---

## 2026-08-07

### Completed
- Built `MenuItem` CRUD API using DRF generic views.
- Refactored `MenuItemSerializer` using ModelSerializer.
- Handled asymmetric `Category` field serialization (IDs for writes, titles for reads).
- Implemented automated slug collision handling in `MenuItem.save()`.
- Configured single item lookup using slug URLs (`lookup_field = "slug"`).
- Optimized query performance using `select_related("category")`.
- Added filtering (`available`), search (`title`, `description`), and ordering (`title`, `created_at`).
- Enforced `admin/manager-only` write access while keeping GET endpoints public.
- Added explicit `is_authenticated` checks inside `get_queryset()` for guest requests.

### Problems Faced
- Accidental inheritance from `serializers.Serializer` instead of `ModelSerializer`.
- Assigning `source="category.title"` to a writable field, breaking `POST`/`PUT` requests.
- Database integrity errors caused by duplicate slugs.
- N+1 database queries when fetching category details.
- Unsafe `is_staff` checks on unauthenticated (`AnonymousUser`) requests.

### Learned
- Overriding `to_representation()` to separate write payload structure from read JSON output.
- Preventing slug collisions using `exists()` and `exclude(pk=self.pk)` in model `save()`.
- Eliminating N+1 query bottlenecks using `select_related()`.
- DRF Browsable API HTML widgets do not affect raw JSON API behavior.
- Explicitly checking `user.is_authenticated` before evaluating user role attributes.