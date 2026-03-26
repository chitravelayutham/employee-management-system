from app.config.database import users_collection
from datetime import datetime

# Create user
def create_user(user_data: dict):
    return users_collection.insert_one(user_data)

# Get user by username
def get_user_by_username(username: str):
    return users_collection.find_one({"username": username})


# Update activity log
def update_user_activity(username: str, action: str):
    return users_collection.update_one(
        {"username": username},
        {
            "$push": {
                "activitylog": {
                    "action": action,
                    "timestamp": datetime.now()
                }
            }
        }
    )