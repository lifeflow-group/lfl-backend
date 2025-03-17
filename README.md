# LifeFlow Backend

## Overview
The LifeFlow Backend project functions as a server-side platform that handles business logic, API services, and database management. It analyzes user performance and habit data, utilizing AI to provide personalized recommendations, explain the benefits behind each suggestion, and deliver actionable insights to enhance user habits.

## Project Structure
```
lfl_backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       ├── routes_habit.py          # Endpoints for habit-related operations
│   │       └── routes_suggestion.py     # Endpoints for suggestion-related operations
│   ├── models/
│   │   ├── habit.py                     # Habit model
│   │   ├── habit_category.py            # Habit category model
│   │   ├── performance_metric.py        # Performance metric model
│   │   ├── suggestion.py                # Suggestion model
│   │   └── user.py                      # User model
│   ├── schemas/
│   │   ├── habit_schema.py              # Schemas for habit-related data
│   │   ├── habit_category_schema.py     # Schemas for habit category data
│   │   ├── performance_metric_schema.py # Schemas for performance metric data
│   │   ├── suggestion_schema.py         # Schemas for suggestion data
│   │   └── user_schema.py               # Schemas for user data
│   ├── services/
│   │   ├── ai_client.py                 # AI client for generating suggestions
│   │   ├── habit_service.py             # Service logic for habits
│   │   └── suggestion_service.py        # Service logic for suggestions
│   ├── dependencies.py                  # Dependency injection
│   ├── database.py                      # DB connection setup
│   ├── config.py                        # Configuration settings
│   └── main.py                          # FastAPI app launcher
├── scripts/
│   ├── setup_database.py                # Initialize DB (users, habits, suggestions)
│   └── drop_database.py                 # Drop the database or tables
├── .env                                 # Secrets & API keys (Gemini, DB)
├── run.py                               # App entry point
├── requirements.txt                     # Project dependencies
└── README.md                            # Project documentation
```

## Technology Stack

- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: ORM for database interactions
- **PostgreSQL**: Relational database management system
- **Pydantic**: Data validation and settings management using Python type annotations
- **Uvicorn**: ASGI server for serving FastAPI applications
- **Google Cloud**: For accessing the Gemini API

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Google Cloud account (for Gemini API access)

### Environment Configuration
1. Clone the repository:
   ```sh
   git clone git@gitlab.com:azvn/nextlevel/lfl-backend.git lfl_backend

   cd lfl_backend
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv env

   env\Scripts\activate        # Windows

   source env/bin/activate         # macOS / Linux
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Copy the `.env.example` file and rename it to `.env`.
   ```sh
   cp .env.example .env
   ```

   Edit .env file
   ```
   DATABASE_URL=postgresql://lfl_user:lfl_password@localhost:5432/lfl_db
   GEMINI_API_KEY=your_gemini_api_key
   ```

### Database Setup
1. Create PostgreSQL user and database:
   ```sh
   psql -U postgres

   CREATE USER lfl_user WITH PASSWORD 'lfl_password';

   CREATE DATABASE lfl_db OWNER lfl_user;

   GRANT ALL PRIVILEGES ON DATABASE lfl_db TO lfl_user;

   \c lfl_db

   GRANT ALL ON SCHEMA public TO lfl_user;

   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO lfl_user;

   \q
   ```

2. Verify database connection:
   ```sh
   psql -U lfl_hoan -d lfl_db
   \q
   ```

3. Initialize the database:
   ```sh
   python scripts/setup_database.py --admin-user postgres --admin-password your_password
   ```

4. Dropping the Database
If you need to drop the database for any reason (e.g., to reset the database schema or start fresh), you can use the drop_database.py script.

a. Run the drop_database.py script to drop the entire database:
   ```sh
   python scripts/drop_database.py --admin-user postgres --admin-password your_password --drop-type database
   ```

b Run the drop_database.py script to drop all tables in the current database schema:
   ```sh
   python scripts/drop_database.py --admin-user postgres --admin-password your_password --drop-type tables
   ```

### Running the Application
1. Start the FastAPI server:
   ```sh
   python run.py
   ```

2. The API will be available at `http://localhost:8000`
3. Access the Swagger documentation at `http://localhost:8000/docs`

## API Documentation

### Endpoints

#### POST /api/habits/analyze
Analyze a set of habits and generate personalized suggestions.

**Request Body Example:**
File habits_500.json

#### GET /api/suggestions/{user_id}
Returns personalized AI-generated suggestions for a user based on their habits.

User id Example: hoan

## Troubleshooting

### Common Issues
- Database connection errors: Verify PostgreSQL is running and credentials are correct
- Gemini API errors: Check API key and quota limits
- Missing dependencies: Ensure all packages from requirements.txt are installed

