from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from auth import create_access_token, verify_token

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dummy user
USER_DB = {
    "sowmi": "password123"
}

# -------------- FIX: Login Request Model ------------------
class LoginRequest(BaseModel):
    username: str
    password: str
# ----------------------------------------------------------

@app.post("/login")
def login(request: LoginRequest):
    username = request.username
    password = request.password

    if username not in USER_DB or USER_DB[username] != password:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token = create_access_token({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token Invalid or Expired")

    return {"message": f"Hello {payload['sub']}, JWT validation success!"}
