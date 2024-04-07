// fetch data from FastAPI endpoint
export const getGeoJson = async (weeks_back) => {
  try {
    const response = await fetch(`http://localhost:8000/geojson?weeks_back=${weeks_back}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching incidents: ', error);
  }
}