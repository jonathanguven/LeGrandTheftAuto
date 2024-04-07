// fetch data from FastAPI endpoint
export const getGeoJson = async (weeks_back) => {
  try {
    let num_weeks = 1;
    if (weeks_back) {
      num_weeks = weeks_back;
    }
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/geojson?weeks_back=${num_weeks}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching incidents: ', error);
  }
}