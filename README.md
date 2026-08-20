# LibNest API

LibNest is a multi-tenant library management REST API built with FastAPI and MongoDB.

## Ownership model

One shared MongoDB database is used. Documents carry explicit ownership fields:

- `college_id` for college-scoped ownership.
- `library_id` for library-scoped ownership.

Libraries belong to exactly one college. Library data is always isolated by `library_id`; college-level actions are isolated by `college_id`.

## Feature layout

Each business capability lives in `app/features/<feature>/`. A feature owns its API router, schemas, service layer, and repository layer. Shared infrastructure belongs in `app/core/`.

For the first release, book inventory is tracked on the book document with `total_copies`, `available_copies`, and `issued_copies`. A separate physical-copy collection can be introduced later if barcode, location, condition, or per-copy history becomes necessary.

## Local setup

```powershell
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Swagger UI will be available at `http://127.0.0.1:8000/docs`.

