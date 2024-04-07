from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
from db.supabase import create_supabase_client
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
  return get_last_month_incidents()

@app.get("/geojson")
async def get_geojson():
  rows = get_last_month_incidents()
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

def get_last_month_incidents():
  # Specify the columns you want to fetch
  columns = 'Incident Date, Incident Time, Latitude, Longitude, Incident ID, Incident Description, Analysis Neighborhood, Incident Subcategory, Incident Datetime'

  # Calculate the date one month back from today
  one_month_back = datetime.now() - relativedelta(months=1)
  
  # Format the date as string in 'YYYY-MM-DD' format (adjust as necessary)
  formatted_date = one_month_back.strftime('%Y/%m/%d')
  formatted_end_date = datetime.now().strftime('%Y/%m/%d')

  # Execute the query with a filter for dates within the last month
  # Assuming 'Incident Date' is stored in a format that Supabase can directly compare (e.g., 'YYYY-MM-DD')
  data, count = supabase.table('incidents')\
                            .select(columns)\
                            .gte('Incident Date', formatted_date)\
                            .lte('Incident Date', formatted_end_date)\
                            .execute()
  return data[1]

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)