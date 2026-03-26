from fastapi import APIRouter
from app.schemas.user_schema import UserCreate, UserLogin
from app.controller.user_controller import register_user, login_user
from app.utils.utils import get_current_user, role_required, admin_required
from fastapi import Depends, HTTPException, status

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    return register_user(user)


@router.post("/login")
def login(user: UserLogin):
    return login_user(user)


#Placeholders for future user-related endpoints (e.g., profile, activity log, etc.)
# 🔒 Admin-only route
@router.get("/admin-dashboard")
def admin_dashboard(user=Depends(admin_required)):
    return {"message": f"Welcome Admin {user['username']}"}


# 🔒 Admin + User access
@router.get("/profile")
def user_profile(user=Depends(role_required(["admin", "user"]))):
    return {
        "username": user["username"],
        "role": user["role"]
    }


# 🔒 Any authenticated user
@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return user