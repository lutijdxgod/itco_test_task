# Secret Storing API

A FastAPI application for one-time access to encrypted secrets. Secrets are automatically deleted after the first view or when the TTL (Time-To-Live) expires.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — modern Python web framework for building APIs
- [PostgreSQL](https://www.postgresql.org/) — database for storing secrets and access logs
- [Redis](https://redis.io/) — cache layer for temporary secret keys
- [Docker & Docker Compose](https://docs.docker.com/) — containerization and easy local deployment
- [SQLAlchemy 2](https://docs.sqlalchemy.org/) — ORM for interacting with the database
- [Alembic](https://alembic.sqlalchemy.org/) — migrations for the database schema
- [JWT Auth](https://jwt.io/) — secure user authentication

---

### 1. Clone the repository

```bash
cd project_directory
git clone https://github.com/lutijdxgod/secret-storing-api.git .
```

### 2. Create the `.env` file

Make a `.env` file in the root of the project and fill it according to `.env.example`:


`CRYPTO__KEY` must be a valid URL-safe base64 string. Generate it in Python like this:
```python
import base64, os
print(base64.urlsafe_b64encode(os.urandom(32)).decode())
```

### 3. Create the `alembic.ini` file

Make a `alembic.ini` file in the root of the project and fill it according to `alembic.ini`:

### 4. Run the application

```bash
docker compose up --build
```

The app will be available at [http://localhost:8000](http://localhost:8000)

---

## API Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
