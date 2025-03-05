from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from pydantic import BaseModel

app = FastAPI()
security = HTTPBearer()

class User(BaseModel):
    email: str
    password: str

@app.post("/register/")
async def register(user: User):
    try:
        user_record = auth.create_user(email=user.email, password=user.password)
        return {"message": "User created successfully", "uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login/")
async def login(user: User):
    try:
        # Firebase REST API or custom token logic can be used here
        # For simplicity, we assume the frontend handles Firebase Auth
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/user/")
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        return {"email": user.email, "uid": user.uid}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")