// fetch data from FastAPI endpoint
export const getGeoJson = async () => {
  try {
    const response = await fetch('http://localhost:8000/geojson');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching incidents: ', error);
  }
}