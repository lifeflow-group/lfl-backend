from fastapi import FastAPI
from app.api.endpoints import routes_habit, routes_suggestion
from app.database import engine, Base
from app.models import *

# Initialize FastAPI app
app = FastAPI(
    title="LFL Backend API",
    description="API cho Habit Analysis và Suggestion",
    version="1.0.0"
)

# Create database tables (use with caution if migrations exist)
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(routes_suggestion.router)
app.include_router(routes_habit.router)
