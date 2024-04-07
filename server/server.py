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
  data, count = supabase.table('incidents').select('*', count='exact').execute()
  return data[1]

@app.get("/geojson")
async def get_geojson():
  data, count = supabase.table('incidents').select('*').execute()
  rows = data[1]
  features = []
  for row in rows:
    try:
      lat = float(row['Latitude'])
      lon = float(row['Longitude'])
      feature = {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [lon, lat]
        },
        "properties": {
          "id": row['Incident ID'],
          "neighborhood": row['Analysis Neighborhood'],
          "category": row['Incident Subcategory'],
          "date": row['Incident Date'],
          "time": row['Incident Datetime'],
          "description": row['Incident Description'],
        }
      }
      features.append(feature)
    except (TypeError, ValueError):
      continue
  geojson = {
    "type": "FeatureCollection",
    "features": features
  }
  return geojson

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)