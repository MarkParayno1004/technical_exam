# Address Book API

A production-ready FastAPI address book service with CRUD operations and geographic proximity search.

## Features

- Full CRUD for addresses (`name`, `street`, `city`, `state`, `zip_code`, `latitude`, `longitude`)
- Proximity search using the `haversine` library (kilometers)
- Pydantic validation for coordinates and request bodies
- SQLite persistence via SQLAlchemy
- Structured logging for requests, DB operations, and errors
- Swagger UI at `/docs`

## Quickstart

```bash
# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file (optional; defaults work out of the box)
cp .env.example .env

# Run the API
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

## API Usage Examples

### Create an address

```bash
curl -X POST "http://127.0.0.1:8000/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Home",
    "street": "123 Main St",
    "city": "Springfield",
    "state": "IL",
    "zip_code": "62701",
    "latitude": 39.7817,
    "longitude": -89.6501
  }'
```

### Get an address by ID

```bash
curl "http://127.0.0.1:8000/addresses/1"
```

### Update an address

```bash
curl -X PUT "http://127.0.0.1:8000/addresses/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Office",
    "street": "456 Oak Ave",
    "city": "Chicago",
    "state": "IL",
    "zip_code": "60601",
    "latitude": 41.8781,
    "longitude": -87.6298
  }'
```

### Search by proximity (within 50 km)

```bash
curl "http://127.0.0.1:8000/addresses/search?latitude=39.7817&longitude=-89.6501&distance=50"
```

### Delete an address

```bash
curl -X DELETE "http://127.0.0.1:8000/addresses/1"
```

## Project Structure

```
app/
  main.py           # Application entry point
  api/              # Route handlers
  models/           # SQLAlchemy models and DB session
  schemas/          # Pydantic request/response models
  core/             # Config, logging, exceptions
  services/         # Business logic and distance calculations
```

## Configuration

Settings are loaded from `.env` via `python-dotenv` / `pydantic-settings`:

| Variable       | Default                          | Description              |
|----------------|----------------------------------|--------------------------|
| `DATABASE_URL` | `sqlite:///./address_book.sqlite`| SQLAlchemy database URL  |
| `APP_NAME`     | `Address Book API`               | Application title        |
| `LOG_LEVEL`    | `INFO`                           | Logging level            |
| `DEBUG`        | `false`                          | Debug mode flag          |
# technical_exam
