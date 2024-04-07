// fetch data from FastAPI endpoint
export const getGeoJson = async (weeks_back) => {
  try {
    let num_weeks = 1;
    if (weeks_back) {
      num_weeks = weeks_back;
    }
    const response = await fetch(`http://localhost:8000/geojson?weeks_back=${num_weeks}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching incidents: ', error);
  }
}