#Bootstrap employee management system backend
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.database import client
from app.routes.employee_routes import router as employee_router
from app.routes.user_routes import router as user_router
from fastapi.middleware.cors import CORSMiddleware

#Importing the context manager for lifespan events startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    try:
        info = client.server_info()  # Attempt to connect to MongoDB
        print("Connected to MongoDB:")
        # Initialize database connection or other resources here

        print("Starting up the Employee Management System API...")
        # For example, you could connect to MongoDB here using the MONGO_URI from .env 
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        # Handle connection error (e.g., retry logic, exit, etc.)
        raise e  # Re-raise the exception after logging 
    yield
    # Shutdown code
    print("Shutting down the Employee Management System API...")

app = FastAPI(title="Employee Management System API", version="1.0", lifespan=lifespan)

app.add_middleware( # To enable CORS for frontend-backend communication during development to avoid 405 Method Not Allowed.
    CORSMiddleware,
    allow_origins=["http://3.80.136.36:3000"],   # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(employee_router, prefix="/employees") #Include employee-related routes
app.include_router(user_router, prefix="/auth") #Include user authentication routes

#Health check endpoint
@app.get("/health")
def health_check(): 
    return {"status": "API is healthy"}