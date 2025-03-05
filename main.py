from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from firebase import initialize_firebase, verify_firebase_token
from database import get_db_connection

app = FastAPI()
security = HTTPBearer()

# Initialize Firebase
initialize_firebase()

# Models
class User(BaseModel):
    email: str
    password: str

# Endpoints
@app.get("/")
def root():
    return {"Hello World"}

@app.post("/register/")
async def register(user: User):
    try:
        # Hash the password (use a library like `passlib`)
        password_hash = hash_password(user.password)

        # Save user to the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
            (user.email, password_hash))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"message": "User created successfully", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login/")
async def login(user: User):
    try:
        # Firebase handles login on the frontend, so this is just a placeholder
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/user/")
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        decoded_token = verify_firebase_token(token)
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        return {"email": user.email, "uid": user.uid}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")