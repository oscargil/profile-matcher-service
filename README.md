# Gameloft Technical Test – Profile Matcher Service

## Overview
This project is a Django-based microservice for matching player profiles to active campaigns, using a fully relational PostgreSQL database. The service exposes endpoints to retrieve player profiles, campaigns, and to match a player to campaigns based on complex rules.

## Architecture

This project follows a **layered architecture** to ensure maintainability, testability, and separation of concerns:

- **API Layer:**
  - Composed of Django Rest Framework views and serializers (`matcher/views.py`, `matcher/serializers.py`).
  - Handles HTTP requests, validation, and serialization of data for the API.
  - Views are kept thin and delegate business logic to the service layer.

- **Service/Business Logic Layer:**
  - Encapsulated in `matcher/services.py`.
  - Contains all business rules and logic, such as the player-to-campaign matching algorithm.
  - This layer is independent of HTTP and can be tested or reused easily.

- **Data/Repository Layer:**
  - Defined by Django ORM models in `matcher/models.py`.
  - Handles all data persistence and relationships.
  - Custom queries or data access logic can be implemented as model managers or in a `repositories.py` module if needed.

**Benefits:**
- Each layer has a single responsibility.
- Business logic is decoupled from HTTP and data access.
- The codebase is easier to test, extend, and maintain.

## Extensibility and Design Patterns

The matching logic uses the **Strategy Pattern** for extensibility and maintainability:

- Each matching rule (e.g., level, has, does_not_have) is implemented as a separate strategy class in `matcher/matchers.py`.
- The service layer (`matcher/services.py`) orchestrates these strategies, applying all of them to determine if a player matches a campaign.
- **To add a new matching rule:**
  1. Create a new strategy class inheriting from `BaseMatcherStrategy` in `matcher/matchers.py`.
  2. Add an instance of this class to the `strategies` list in the service function.
- This approach allows new rules to be added with minimal changes to the core logic, improving extensibility and testability.

## Features
- Django + Django Rest Framework backend
- PostgreSQL database (via Docker)
- Fully relational models (no JSON fields)
- Campaign matching logic faithful to business requirements
- Endpoints for listing players, campaigns, and matching a player to campaigns
- Dockerized for easy setup and deployment
- **Automatic API documentation with Swagger and ReDoc (drf-yasg)**

## Requirements
- Docker & Docker Compose
- (Optional) Python 3.12+ and virtualenv for local development

## Setup (with Docker)

1. **Build and start the services:**
   ```sh
   docker compose build
   docker compose up
   ```

2. **Apply migrations and initialize example data:**
   In a new terminal:
   ```sh
   docker compose exec web python manage.py migrate
   docker compose exec web python initialize_data.py
   ```

3. **(Optional) Create a superuser for Django admin:**
   ```sh
   docker compose exec web python manage.py createsuperuser
   ```

4. **Access the service:**
   - API: [http://localhost:8000/](http://localhost:8000/)
   - Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## API Documentation

- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- **OpenAPI JSON:** [http://localhost:8000/swagger.json](http://localhost:8000/swagger.json)

The documentation is automatically generated from Django Rest Framework views and serializers using [drf-yasg](https://drf-yasg.readthedocs.io/).

## API Endpoints

- **GET /players/**
  - List all player profiles (with nested devices, inventory, clan, and active campaigns)

- **GET /campaigns/**
  - List all campaigns (with nested matchers: level, has, does_not_have)

- **GET /get_client_config/{player_id}/**
  - Returns the full profile for the given player, updates active campaigns if the player matches any campaign's rules

## Data Model
- All data is stored in PostgreSQL using Django ORM models.
- Example data (one player, one campaign) is loaded by running `initialize_data.py`.

## Unit Tests

This project includes **unit tests for the matching logic** (the `matcher` module) as a demonstration. The tests cover the main cases of the player-to-campaign matching algorithm, using `pytest` and `pytest-django`.

- The tests are located in `matcher/tests/test_services.py`.
- Only the business logic (service layer) is tested, not endpoints or full integration.
- You can easily extend them to cover more rules or logic.

### Run tests with Docker Compose

You can run all unit tests easily with:

```sh
# Runs the tests in an isolated container and removes the container when done

docker compose run --rm test
```

This runs `pytest` inside the Docker environment, using the PostgreSQL database defined in `docker-compose.yml`.

## Notes

- By default, the example data does not match any campaign because the campaign's end date is in the past. You can change the campaign's end date in the Django admin to a future date to verify that the matching works as expected in production.
- This scenario (matching with valid dates) is also covered by the unit tests for the business logic.

---

**Author:** Oscar Gil Sotillo
