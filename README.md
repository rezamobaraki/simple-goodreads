# Simple Goodreads API

A simplified model of the Goodreads API built using Django and Django REST Framework (DRF). This project includes
features like book ratings, reviews, and bookmarking, offering basic API functionality for managing books and user
interactions with them.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Docker Usage](#docker-usage)
- [Environment Variables](#environment-variables)
- [Makefile Commands](#makefile-commands)
- [Seed Data](#seed-data)
- [Data](#data)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Contact](#contact)

## Project Overview

The `Simple Goodreads API` project allows users to interact with books, review them, add reviews, and bookmark
favorites. It also supports user authentication with JWT tokens. The project uses Docker for easy deployment and comes
with an auto-generated Swagger UI for API documentation.

## Features

- User authentication (JWT)
- Book management (list, retrieve, bookmark)
- Book reviews and ratings
- **Book Statistics**: Automatically calculates and caches book statistics such as review count, rating count, average
  rating, and rating distribution.
    - In addition, I outlined the New Methods for the BookStat model, including:`update_or_create_stat`
      `get_or_calculate_stats`
- **signals**: Automatically updates book statistics when a review is added or deleted. `calculate_stats_signal`
- **Caching**: Utilizes Django's caching framework to cache results of various functions for improved performance.
- **Fraud Detection**: Detects suspicious activity based on the number of rating actions within a certain time frame.
- Swagger UI and Redoc for API documentation
- Dockerized for easy setup and deployment

## Project Structure

```
.
├── Dockerfile
├── Makefile
├── README.md
├── config.env
├── config.example.env
├── docker-compose.yaml
├── src/
│   ├── accounts/
│   ├── books/
│   │   ├── models/
│   │   │   ├── book.py
│   │   │   ├── bookmark.py
│   │   │   ├── review.py
│   │   │   └── stat.py
│   │   ├── services/
│   │   │   ├── commands/
│   │   │   │   └── review.py
│   │   │   ├── queries/
│   │   │   │   └── review.py
│   │   └── signal.py
│   ├── commons/
│   │   └── fraud_detection.py
│   ├── core/
│   │   ├── celery.py
│   │   ├── settings/
│   │   │   ├── django/
│   │   │   │   └── base.py
│   │   │   ├── third_parties/
│   │   │   │   ├── cache.py
│   │   │   │   ├── fraud_config.py
│   │   │   │   └── redis_templates.py
│   ├── fixtures/
│   ├── manage.py
│   └── routers/
```

- `accounts/`: Handles user authentication and registration.
- `books/`: Manages books, reviews, ratings, bookmarks, and book statistics.
- `commons/`: Common utilities, including fraud detection.
- `core/`: Core settings, configurations, and entry points.
- `fixtures/`: Predefined data for database seeding.
- `routers/`: API routing and versioning.

## Setup and Installation

### Requirements

- Docker
- Docker Compose
- Python 3.8+
- Poetry (for dependency management)

### Local Development

1. Clone the repository:

   ```bash
   git clone https://github.com/MrRezoo/simple-goodreads.git
   cd simple-goodreads
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Set up the environment variables:

   ```bash
   cp config.example.env config.env
   ```

4. Start the development server:

   ```bash
   make runserver
   ```

### Using Docker

1. Prepare the Docker environment:

   ```bash
   make prepare-compose
   ```

2. Start the Docker containers:

   ```bash
   make up
   ```

3. To rebuild and start:

   ```bash
   make up-force-build
   ```

4. To stop the containers:

   ```bash
   make down
   ```

## Environment Variables

Ensure the following environment variables are set in the `config.env` file:

```ini
SECRET_KEY = django-insecure
DEBUG = True
LOGLEVEL = info
ALLOWED_HOSTS = 0.0.0.0,127.0.0.1,localhost
POSTGRES_NAME = goodreads
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
POSTGRES_HOST = goodreads_postgres
POSTGRES_PORT = 5432
JWT_SECRET_KEY = your_jwt_secret_key

# Cache settings
REDIS_HOST = localhost
REDIS_PORT = 6379
CACHE_TTL_MINUTES = 15
CACHE_TIMEOUT = 3600

# Fraud detection settings
FRAUD_DETECTION_RATE_LIMIT_PERIOD = 3600
FRAUD_DETECTION_MAX_RATES_PER_HOUR = 500
FRAUD_DETECTION_SUSPICIOUS_THRESHOLD = 1000
FRAUD_DETECTION_TIME_THRESHOLD = 10
FRAUD_DETECTION_LAST_ACTIONS_TO_TRACK = 100
FRAUD_DETECTION_SUSPECTED_RATES_THRESHOLD = 0.2
```

## Makefile Commands

This project uses a `Makefile` to automate common tasks:

| Command                 | Description                                     |
|-------------------------|-------------------------------------------------|
| `make help`             | Show available make commands                    |
| `make install`          | Install all dependencies using Poetry           |
| `make runserver`        | Run Django development server                   |
| `make runserver-plus`   | Run Django server with enhanced debugging tools |
| `make migrate`          | Apply database migrations                       |
| `make make-migration`   | Create new migration files                      |
| `make dump-data`        | Dump the current database data                  |
| `make create-superuser` | Create a Django superuser                       |
| `make db-shell`         | Open the database shell                         |
| `make shell`            | Open Django shell                               |
| `make shell-plus`       | Open enhanced Django shell with SQL logging     |
| `make show-urls`        | Display all registered URLs                     |
| `make test`             | Run tests                                       |
| `make lint`             | Run linters (flake8)                            |
| `make collect-static`   | Collect static files                            |
| `make build`            | Build the Docker image                          |
| `make up`               | Start Docker containers                         |
| `make up-force-build`   | Rebuild and start Docker containers             |
| `make down`             | Stop the Docker containers                      |
| `make prepare-compose`  | Prepare Docker Compose environment              |
| `make seeder`           | Seed the database with initial data             |
| `make load-data`        | Load fixtures data into the database            |

## Seed Data

#### Attention: If you are using Docker-Compose,

```bash
 make seeder ARGS="--user=<user_count> --book=<book_count> --review=<review_count> --bookmark=<bookmark_count>"
```

- In this case, all user passwords are `password`.

Or you can use fixtures data by running the following command:

```bash
 python manage.py loaddata fixtures/<fixture_name>.json
# or
 make load-data ARGS="fixtures/<fixture_name>.json"
```

## Data

The project comes with predefined data for seeding the database. The data includes:

- Users (accounts/fixtures/users.json)
    - Email: `admin@admin.com`, Password: `admin`
    - Email: `rezoo@gmail.com`, Password: `reza1234`
    - Email: `ali@gmail.com`, Password: `ali1234`
    - Email: `maryam@gmail.com`, Password: `mary1234`
    - Email: `shahriar@gmail.com`, Password: `shahr1234`
    - Email: `kimia@gmail.com`, Password: `kimi@1234`

- Books (books/fixtures/books.json)
- Reviews (books/fixtures/reviews.json)
- Bookmarks (books/fixtures/bookmarks.json)

## API Documentation

This project comes with automatically generated API documentation using Swagger and ReDoc.

- **Swagger UI**: Available at `/api/v1/swagger/`
- **ReDoc UI**: Available at `/api/v1/redoc/`

You can also access the API documentation by Postman collection in the `docs` directory.

- **Postman Collection**: Available at `/docs/Goodreads.postman_collection.json`

Example API routes include:

- `GET /api/v1/accounts/auth/` - User registration and authentication.
- `GET /api/v1/books/` - List, Retrieve, bookmark, and Review books.
    - `GET /api/v1/books/{id}/` - Retrieve a specific book.
    - `POST /api/v1/books/{id}/bookmark/` - Bookmark a book.
    - `POST /api/v1/books/{id}/review/` - Add a review to a book.

Admin panel is available at `/admin/` with the following credentials:

- Email: `admin@admin.com` Password: `admin`

## Running Tests

To run the tests:

```bash
make test
```

## Contact

For any inquiries or issues, please contact:

- Name: Reza M. (@MrRezoo)
- Email: [rezam578@gmail.com](mailto:rezam578@gmail.com)