# Engineering Decision Log

---

## EDL-001: Create a Core App

### Date
2026-08-02

### Decision
Create a dedicated `core` app for reusable infrastructure.

### Problem
Several apps require shared functionality like timestamp fields, validators, and pagination.

### Alternatives Considered
1. Keep shared code inside the `users` app.
2. Duplicate the code in every app.

### Decision
Create a `core` app.

### Why?
- Reduces code duplication.
- Keeps business apps independent.
- Improves maintainability.

### Trade-offs
- One additional app to maintain.

### Future Improvements
Move additional reusable components such as custom managers and utilities into `core` as needed.

---

## EDL-002: Use an Abstract TimeStampedModel

### Decision
Create an abstract `TimeStampedModel`.

### Why?
Avoid repeating `created_at` and `updated_at` in every model.

### Alternatives
- Duplicate fields in every model.
- Multi-table inheritance.

### Trade-offs
One extra inheritance layer for cleaner, DRYer code.