import requests
import pandas as pd
import matplotlib.pyplot as plt

# The URL of the endpoint
url = 'http://127.0.0.1:8000/getIncidents'

# Make a GET request to the endpoint
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response data (assuming it's JSON)
    data = response.json()
    #print(data['data'][0]['Latitude'])

    # Now you can use the data object for analysis
else:
    print(f"Failed to retrieve data: {response.status_code}")

# Example structure: [{'latitude': 37.7749, 'longitude': -122.4194}, ...]

# Extract latitude and longitude values
latitudes =[data['data'][i]['Latitude'] for i in range(len(data['data']))]
longitudes =[data['data'][i]['Longitude'] for i in range(len(data['data']))]
print(latitudes)
print(longitudes)
plt.figure(figsize=(8,12))

# Scatter plot with alpha for transparency and s for size of the point
plt.scatter(longitudes, latitudes, alpha=0.6, s=10)

# Setting axis labels and plot title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Geographical Distribution of Incidents')

# Ensuring the aspect ratio is equal to prevent distortion
plt.gca().set_aspect('equal', adjustable='box')

plt.show()

