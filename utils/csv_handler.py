import csv
import os
from passlib.context import CryptContext
from typing import List, Optional
from models import User, BoneDensityResult

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

DATA_DIR = "data"
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
RESULTS_CSV = os.path.join(DATA_DIR, "results.csv")

def init_csvs():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "email", "hashed_password"])
    if not os.path.exists(RESULTS_CSV):
        with open(RESULTS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "user_email", "age", "weight_kg", "height_cm", "gender", "activity_level", "t_score", "bmi", "interpretation", "risk_category"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_user(email: str) -> Optional[User]:
    print("email", email)
    if not os.path.exists(USERS_CSV):
        return None
    with open(USERS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print("row", row)
            if row["email"] == email:
                return User(id=int(row["id"]), email=row["email"], hashed_password=row["hashed_password"])
    return None

def create_user(email: str, password: str) -> int:
    user_id = get_next_user_id()
    hashed = hash_password(password)
    with open(USERS_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, email, hashed])
    return user_id

def get_next_user_id() -> int:
    if not os.path.exists(USERS_CSV):
        return 1
    with open(USERS_CSV, 'r') as f:
        reader = list(csv.reader(f))
        return len(reader)

def save_result(user_email: str, input_data: dict, result_obj):
    # Delete existing records for this user
    lines = []
    if os.path.exists(RESULTS_CSV):
        with open(RESULTS_CSV, 'r') as f:
            reader = csv.DictReader(f)
            lines = [row for row in reader if row['user_email'] != user_email]
    
    # Append new record
    next_id = get_next_result_id()
    lines.append({
        'id': next_id,
        'user_email': user_email,
        'age': input_data['age'],
        'weight_kg': input_data['weight_kg'],
        'height_cm': input_data['height_cm'],
        'gender': input_data['gender'],
        'activity_level': input_data['activity_level'],
        't_score': result_obj.t_score,
        'bmi': result_obj.bmi,
        'interpretation': result_obj.interpretation,
        'risk_category': result_obj.risk_category
    })
    
    # Rewrite CSV
    with open(RESULTS_CSV, 'w', newline='') as f:
        if lines:
            fieldnames = lines[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(lines)

def get_next_result_id() -> int:
    if not os.path.exists(RESULTS_CSV):
        return 1
    with open(RESULTS_CSV, 'r') as f:
        reader = list(csv.reader(f))
        return len(reader)

from fastapi import Request, HTTPException
from models import User

def get_current_user(request: Request) -> User:
    user_email = request.cookies.get("user_email")
    if not user_email:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user(user_email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def get_last_result(user_email: str) -> Optional[dict]:
    if not os.path.exists(RESULTS_CSV):
        return None
    results = []
    with open(RESULTS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_email"] == user_email:
                results.append(row)
    if not results:
        return None
    # Latest by id desc
    results.sort(key=lambda x: int(x["id"]), reverse=True)
    return results[0]
