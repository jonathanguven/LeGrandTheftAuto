<script>
  import mapboxGl from 'mapbox-gl';
  import "../../node_modules/mapbox-gl/dist/mapbox-gl.css";
  import { onMount, onDestroy } from "svelte";
  import { getGeoJson } from '../apiFunctions/getGeoJson';

  let data;

  let dark = true;
  $: theme = dark ? 'dark' : 'light';
  $: style = `mapbox://styles/mapbox/${theme}-v11`;

  $: {
    if (map) {
      map.setStyle(style);
    }
  }

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

  onMount(async () => {
    data = await getGeoJson();
    console.log(data);
    const initialState = { lng: lng, lat: lat, zoom: zoom };

    map = new mapboxGl.Map({
      container: mapContainer,
      accessToken: import.meta.env.VITE_MAPBOX_TOKEN,
      style,
      center: [initialState.lng, initialState.lat],
      zoom: initialState.zoom,
    });

    map.on('load', () => {
      map.addSource('incidents', {
        type: 'geojson',
        data: data
      });
      
      map.addLayer({
        id: 'incidents',
        type: 'heatmap',
        source: 'incidents',
        maxzoom: 15,
        paint: {
          'heatmap-weight': {
            type: 'exponential',
            stops: [
              [1,0.2],
              [62, 1]
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
      },
      'waterway-label'
      );

      map.addLayer(
  {
    id: 'incidents2',
    type: 'circle',
    source: 'incidents',
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
  },
  'waterway-label'
      );
      map.on('click', 'incidents2', (event) => {
        new mapboxGl.Popup()
          .setLngLat(event.features[0].geometry.coordinates)
          .setHTML(`<strong>incident:</strong> ${event.features[0].properties.description} <br> <strong>date of incident: </strong>${event.features[0].properties.date}`)
          .addTo(map);
      });
    });

    map.on('move', () => {
      updateData();
    });

  });

  onDestroy(() => {
    map.remove();
  });

</script>

<head>

</head>

<div class="sidebar">
  Longitude: {lng.toFixed(4)} | Latitude: {lat.toFixed(4)} | Zoom: {zoom.toFixed(2)}
</div>
<!-- <input type="checkbox" class="toggle mode" bind:checked={dark}/> -->
<div class="w-full h-full absolute">
  <div class="w-full h-full" bind:this={mapContainer} />
</div>

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

</style>