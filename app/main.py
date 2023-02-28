from fastapi import Depends, FastAPI, HTTPException, Request

from typing import List
from .schemas import User, UserCreate, UserUpdate

app = FastAPI()


@app.get("/")
def read_root():
    return "Welcome to the data sync app :)"


# Mock database of users
users_db = [
    {"id": "1", "name": "Alice", "age": 25},
    {"id": "2", "name": "Bob", "age": 30},
    {"id": "3", "name": "Charlie", "age": 35},
]


@app.get("/users", response_model=List[User])
async def read_users():
    """
    Retrieve all users.
    """
    return users_db


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str):
    """
    Retrieve a user by ID.
    """
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """
    Create a new user.
    """
    user_dict = user.dict()
    user_dict["id"] = str(len(users_db) + 1)
    users_db.append(user_dict)
    return user_dict


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserUpdate):
    """
    Update a user by ID.
    """
    for db_user in users_db:
        if db_user["id"] == user_id:
            update_data = user.dict(exclude_unset=True)
            updated_user = {**db_user, **update_data}
            users_db[users_db.index(db_user)] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")
