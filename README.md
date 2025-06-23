# Profile Matcher Service

A simple FastAPI service to match player profiles with active campaigns based on configurable rules.

## Features
- Retrieves player profiles from a mock database (JSON file).
- Loads current campaigns from a JSON file.
- Matches player profiles against campaign rules (level, country, items, etc.).
- Updates the player's active campaigns if they qualify.
- Exposes a REST API endpoint to get the updated player profile.
- Includes unit tests for the core matching logic.

## Project Structure
```
.
├── main.py                # FastAPI app and endpoint
├── services.py            # Business logic and data access
├── models.py              # Pydantic models
├── campaign_data.json     # Mock campaign data
├── player_profile.json    # Mock player data
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose setup
├── test_services.py       # Unit tests for matching logic
└── README.md              # Project documentation
```

## Requirements
- Docker
- Docker Compose
- Python dependencies (installed automatically in the container):
  - fastapi
  - uvicorn[standard]
  - pydantic
  - pytest

## How to Run the Service

1. **Build and start the service using Docker Compose:**
   ```sh
   docker compose up --build
   ```
   This will build the image and start the FastAPI server inside a container.

2. **Access the API:**
   - The service will be available at: `http://localhost:8000`
   - Example endpoint:
     ```
     GET /get_client_config/{player_id}
     ```
   - Example:
     ```sh
     curl http://localhost:8000/get_client_config/97983be2-98b7-11e7-90cf-082e5f28d836
     ```

## API Documentation

Once the service is running, you can access the interactive Swagger UI documentation at:

- [http://localhost:8000/docs](http://localhost:8000/docs)

Or the alternative ReDoc documentation at:

- [http://localhost:8000/redoc](http://localhost:8000/redoc)


## How to Run Unit Tests in Docker

1. **Make sure the service is built and running:**
   ```sh
   docker compose up --build
   ```

2. **Open a bash shell inside the running container:**
   ```sh
   docker compose exec profile-matcher-api /bin/bash
   ```

3. **Run the tests:**
   ```sh
   pytest test_services.py
   ```
   This will execute all unit tests and print the results in the terminal.

4. **Exit the container:**
   ```sh
   exit
   ```

## Notes
- All configuration and data are stored in JSON files for simplicity.
- The service and tests are fully containerized; no Python installation is needed on your host.

## Author
- Oscar Gil Sotillo
