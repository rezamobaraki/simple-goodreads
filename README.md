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
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Contact](#contact)

## Project Overview

The `Simple Goodreads API` project allows users to interact with books, rate them, add reviews, and bookmark favorites.
It also supports user authentication with JWT tokens. The project uses Docker for easy deployment and comes with an
auto-generated Swagger UI for API documentation.

## Features

- User authentication (JWT)
- Book management (list, retrieve, bookmark)
- Book reviews and ratings
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
│   ├── accounts/
│   ├── books/
│   ├── commons/
│   ├── core/
│   ├── fixtures/
│   ├── manage.py
│   └── routers/
```

- `accounts/`: Handles user authentication and registration.
- `books/`: Manages books, reviews, ratings, and bookmarks.
- `commons/`: Common utilities and middlewares.
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
POSTGRES_PORT = 5433
JWT_SECRET_KEY = your_jwt_secret_key
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

## API Documentation

This project comes with automatically generated API documentation using Swagger and ReDoc.

- **Swagger UI**: Available at `/api/v1/swagger/`
- **ReDoc UI**: Available at `/api/v1/redoc/`

Example API routes include:

- `GET /api/v1/accounts/` - User registration and authentication.
- `GET /api/v1/books/` - Retrieve, bookmark, and rate books.

## Running Tests

To run the tests, execute:

```bash
make test
```

## License

This project is licensed under the BSD License.

## Contact

For any inquiries or issues, please contact:

- Name: Reza M.
- Email: rezam578@gmail.com