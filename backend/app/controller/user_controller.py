from fastapi import HTTPException, status
from app.model.user_model import create_user, get_user_by_username, update_user_activity
from app.utils.utils import hash_password, verify_password, create_access_token

# Register new user
def register_user(user):
    existing_user = get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["activitylog"] = []

    create_user(user_dict)

    update_user_activity(user.username, "User Registered")

    return {"message": "User registered successfully"}



# Login user
def login_user(user):
    db_user = get_user_by_username(user.username)
  
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    update_user_activity(user.username, "User Logged In")

    token = create_access_token({
        "username": db_user["username"],
        "role": db_user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}