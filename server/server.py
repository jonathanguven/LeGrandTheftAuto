from fastapi import FastAPI
import uvicorn 
from db.supabase import create_supabase_client
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

app = FastAPI()
supabase = create_supabase_client()

@app.get("/")
async def index():
  return "Welcome to LeGrandTheftAuto"

@app.get("/getIncidents")
async def get_incidents():
    # Specify the columns you want to fetch
    columns = 'Incident Date, Incident Time, Latitude, Longitude'
  
    # Calculate the date one month back from today
    one_month_back = datetime.now() - relativedelta(months=1)
    
    # Format the date as string in 'YYYY-MM-DD' format (adjust as necessary)
    formatted_date = one_month_back.strftime('%Y/%m/%d')
    formatted_end_date = datetime.now().strftime('%Y/%m/%d')

    # Execute the query with a filter for dates within the last month
    # Assuming 'Incident Date' is stored in a format that Supabase can directly compare (e.g., 'YYYY-MM-DD')
    response = supabase.table('incidents')\
                             .select(columns)\
                             .gte('Incident Date', formatted_date)\
                             .lte('Incident Date', formatted_end_date)\
                             .execute()
    return response

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)