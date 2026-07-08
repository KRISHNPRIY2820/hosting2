from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt

app = FastAPI()

PUBLIC_KEY = """YOUR_PUBLIC_KEY_HERE"""
ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-3uc64lkw.apps.exam.local"

class TokenRequest(BaseModel):
    token: str

@app.post("/verify")
def verify_token(req: TokenRequest):
    try:
        payload = jwt.decode(
            req.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
        )
        return {
            "valid": True,
            "email": payload.get("email"),
            "sub": payload.get("sub"),
            "aud": payload.get("aud"),
        }
    except Exception:
        raise HTTPException(status_code=401, detail={"valid": False})
