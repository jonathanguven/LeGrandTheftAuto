from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
from db.supabase import create_supabase_client

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
supabase = create_supabase_client()

@app.get("/")
async def index():
  return "Welcome to LeGrandTheftAuto"

@app.get("/getIncidents")
async def get_incidents():
  response = supabase.table('incidents').select('*', count='exact').execute()
  return response

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)