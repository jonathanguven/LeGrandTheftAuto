from fastapi import FastAPI
import uvicorn 
from db.supabase import create_supabase_client

app = FastAPI()
supabase = create_supabase_client()

@app.get("/")
async def index():
  return "Welcome to LeGrandTheftAuto"


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)