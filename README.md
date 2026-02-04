# Employee & Attendance Management System

## Project Overview
Backend API for managing employees and their attendance records. Built with FastAPI and Python, designed to be simple and efficient.

## Tech Stack Used
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** SQLite (using SQLAlchemy ORM)
- **Server:** Uvicorn
- **Containerization:** Docker

## Steps to Run the Project Locally

### Prerequisites
- Python 3.10 or higher
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd "hrm backend"
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API documentation at:
   - **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Steps to Run with Docker

1. Build the Docker image:
   ```bash
   docker build -t hrm-backend .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --name hrm-backend-app hrm-backend
   ```

3. Access the application at [http://localhost:8000](http://localhost:8000).

## Assumptions or Limitations
- **Database Persistence:** The project uses SQLite (`sql_app.db`).
  - By default in Docker, the database is stored inside the container. To persist data across container restarts/removals, you need to mount a volume:
    ```bash
    docker run -d -p 8000:8000 -v "/path/to/your/db:/app/sql_app.db" hrm-backend
    ```
- **Configuration:** Database URL is currently hardcoded in `app/database.py`.
