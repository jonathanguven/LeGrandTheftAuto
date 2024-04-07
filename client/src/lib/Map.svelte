<script>
  import mapboxGl from 'mapbox-gl';
  import "../../node_modules/mapbox-gl/dist/mapbox-gl.css";
  import { onMount, onDestroy } from "svelte";
  import { getGeoJson } from '../apiFunctions/getGeoJson';
  import { calculateRecency } from './utils/time.js';

  let data;
  let dark = true;
  let timeFrame = '';
  // let layer = 'incidents';

  $: timeFrame, updateTime();

  $: theme = dark ? 'dark' : 'light';
  $: color = dark ? '#87CEEB' : '#B42222';
  $: style = `mapbox://styles/mapbox/${theme}-v11`;

  let map;
  let mapContainer;
  let lng, lat, zoom;

  lat = 37.76;
  lng = -122.44;
  zoom = 12;

  function updateData() {
    zoom = map.getZoom();
    lng = map.getCenter().lng;
    lat = map.getCenter().lat;
  }

  async function addDataLayer() {
    if (!map.getSource('incidents')) {
      if (!data) data = await getGeoJson();
      map.addSource('incidents', {
        type: 'geojson',
        data: data
      });
    }
    if (!map.getLayer('incidents')) {
      map.addLayer({
        id: 'incidents',
        type: 'circle',
        source: 'incidents',
        paint: {
          'circle-radius': 3,
          'circle-color': `${color}`
        }
      });
    }
  }

  async function addHeatMapLayer() {
    if (!map.getSource('heatSource')) {
      map.addSource('heatSource', {
        type: 'geojson',
        data: data
      });
    }

    if (!map.getLayer('heatIncidents')) {
      map.addLayer({
        id: 'heatIncidents',
        type: 'heatmap',
        source: 'heatSource',
        maxzoom: 15,
        paint: {
          'heatmap-weight': {
            type: 'exponential',
            property: 'recency',
            stops: [
              [0,3],
              [10, 1],
              [20, 0.3],
              [30, 0]
            ]
          },
          //increase intensity as zoom level increases
          'heatmap-intensity': {
            stops: [
              [11,1],
              [15,3]
            ]
          },
          //assign color values be applied to points depending on their density
          'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0,
            'rgba(236,222,239,0)',
            0.2,
            'rgb(200, 0, 10)',
            0.4,
            'rgb(220, 0, 20)',
            0.6,
            'rgb(230, 0, 40)',
            0.8,
            'rgb(255, 0, 99)'
          ],
          //increase radius as zoom increases
          'heatmap-radius': {
            stops: [
              [11,10],
              [15,18]
            ]
          },
          //decrease opacity to transition into the circle layer
          'heatmap-opacity': {
            default: 1,
            stops: [
              [14,1],
              [15,0]
            ]
          }
        }
      });
  
      map.addLayer({
        id: 'heatIncidentsButtons',
        type: 'circle',
        source: 'heatSource',
        minzoom: 14,
        paint: {
          // increase the radius of the circle as the zoom level and dbh value increases
          'circle-radius': {
            property: 'dbh',
            type: 'exponential',
            stops: [
              [{ zoom: 15, value: 1 }, 5],
              [{ zoom: 15, value: 62 }, 10],
              [{ zoom: 22, value: 1 }, 20],
              [{ zoom: 22, value: 62 }, 50]
            ]
          },
          'circle-color': {
            property: 'dbh',
            type: 'exponential',
            stops: [
              [0, 'rgba(236,222,239,0)'],
              [10, 'rgb(236,222,239)'],
              [20, 'rgb(208,209,230)'],
              [30, 'rgb(166,189,219)'],
              [40, 'rgb(103,169,207)'],
              [50, 'rgb(28,144,153)'],
              [60, 'rgb(1,108,89)']
            ]
          },
          'circle-stroke-color': 'white',
          'circle-stroke-width': 1,
          'circle-opacity': {
            stops: [
              [14, 0],
              [15, 1]
            ]
          }
        }
    });

    // When the mouse moves over the 'incidents2' layer, show the popup.
  map.on('mousemove', 'heatIncidentsButtons', (event) => {
    // Check if there is already a popup on the map and if not, create a new one.
    if (!map.getCanvas().style.cursor) {
      map.getCanvas().style.cursor = 'pointer'; // Change the cursor to a pointer

      const coordinates = event.features[0].geometry.coordinates.slice();
      const description = event.features[0].properties.description;
      const date = event.features[0].properties.date;

      // Ensure that if the map is zoomed out such that multiple
      // copies of the feature are visible, the popup appears over the copy
      // being pointed to.
      while (Math.abs(event.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += event.lngLat.lng > coordinates[0] ? 360 : -360;
      }

      // Create a popup and add it to the map.
      new mapboxGl.Popup()
        .setLngLat(coordinates)
        .setHTML(`<strong>Incident:</strong> ${description} <br> <strong>Date of Incident: </strong>${date}`)
        .addTo(map);
    }
  });

  // When the mouse leaves the 'incidents2' layer, remove the popup and reset cursor style.
  map.on('mouseleave', 'heatIncidentsButtons', () => {
    map.getCanvas().style.cursor = ''; // Reset cursor style
    // Remove the popup
    const popups = document.getElementsByClassName('mapboxgl-popup');
    if (popups.length) {
      popups[0].remove();
    }
  });

    }
  }
  function updateVisibility(layer) {
    map.setLayoutProperty('incidents', 'visibility', 'none');
    map.setLayoutProperty('heatIncidents', 'visibility', 'none');
    map.setLayoutProperty('heatIncidentsButtons', 'visibility', layer === "heatIncidents" ? 'visible' : 'none');
    map.setLayoutProperty(layer, 'visibility', 'visible');
    console.log(layer);
    console.log(map.getLayoutProperty(layer, 'visibility'));
  }

  $: {
    if (map) {
      map.setStyle(style);    }
  }

  async function updateTime() {
    let numWeeks = 1;
    if (timeFrame) {
      if (timeFrame === '1 Week') numWeeks = 1;
      if (timeFrame === '1 Month') numWeeks = 4;
      if (timeFrame === '3 Months') numWeeks = 12;
      if (timeFrame === '1 Year') numWeeks = 52;
      data = await getGeoJson(numWeeks);
    } else {
      data = await getGeoJson(1);
    }
    data.features.forEach(feature => {
      const dateString = feature.properties.date; 
      feature.properties.recency = calculateRecency(dateString);
    });
    map.getSource('incidents').setData(data);
    map.getSource('heatSource').setData(data);
    
  }

  onMount(async () => {
    data = await getGeoJson(1);

    const initialState = { lng: lng, lat: lat, zoom: zoom };

    map = new mapboxGl.Map({
      container: mapContainer,
      accessToken: import.meta.env.VITE_MAPBOX_TOKEN,
      style,
      center: [initialState.lng, initialState.lat],
      zoom: initialState.zoom,
    });
    
    map.on('load', async() => { 
      await addDataLayer(); 
      await addHeatMapLayer();
    });
    map.on('styledata', async () => { 
      await addDataLayer(); 
      await addHeatMapLayer();
    });

    map.on('click', 'heatIncidentsButtons', (event) => {
      new mapboxGl.Popup()
        .setLngLat(event.features[0].geometry.coordinates)
        .setHTML(`<strong>incident:</strong> ${event.features[0].properties.description} <br> <strong>date of incident: </strong>${event.features[0].properties.date}`)
        .addTo(map);
    });
    
    map.on('move', () => {
      updateData();
    });
  });

  onDestroy(() => {
    map.remove();
  });
</script>

<main>
  <!-- lat long description -->
  <div class="sidebar">
    Longitude: {lng.toFixed(4)} | Latitude: {lat.toFixed(4)} | Zoom: {zoom.toFixed(2)}
  </div>
  <!-- dark mode toggle -->
  <input type="checkbox" class="toggle mode" bind:checked={dark}/>
  <!-- layer input -->
  <div class="flex justify-between">
    <div class="buttons">
      <button class="btn mr-4" on:click={() => updateVisibility('incidents')}>Points</button>
      <button class="btn mr-4" on:click={() => updateVisibility('heatIncidents')}>HeatMap</button>
    </div>
    <!-- time frame dropdown -->
    <select class="select select-primary w-full max-w-xs m-4 z-10" bind:value={timeFrame}>
      <option disabled selected value="">Time Frame</option>
      <option>1 Week</option>
      <option>1 Month</option>
      <option>3 Months</option>
      <option>1 Year</option>
    </select>
  </div>
  <!-- map container -->
  <div class="w-full h-full absolute -mt-20">
    <div class="w-full h-full" bind:this={mapContainer} />
  </div>
  <p class="absolute z-10 text-white"> Time Frame: {timeFrame}</p>
</main>

<style>
  .sidebar {
    color: #fff;
    padding: 6px 12px;
    font-family: monospace;
    z-index: 1;
    position: absolute;
    bottom: 0;
    left: 0;
    margin: 12px;
    border-radius: 4px;
    background-color: dimgray;
  }
  .mode {
    position: absolute;
    bottom: 0;
    right: 0;
    z-index: 1;
    margin: 18px;
  }
  .buttons {
    position: relative;
    top: 0;
    left: 0;
    z-index: 1;
    margin: 16px;
  }
</style>