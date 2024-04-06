<script>
  import { Map } from 'mapbox-gl';
  import "../../node_modules/mapbox-gl/dist/mapbox-gl.css";

  import { onMount, onDestroy } from "svelte";

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

  onMount(() => {
    const initialState = { lng: lng, lat: lat, zoom: zoom };

    map = new Map({
      container: mapContainer,
      accessToken: import.meta.env.VITE_MAPBOX_TOKEN,
      style,
      center: [initialState.lng, initialState.lat],
      zoom: initialState.zoom,
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
<input type="checkbox" class="toggle mode" bind:checked={dark}/>
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
  .mode {
    position: absolute;
    bottom: 0;
    right: 0;
    z-index: 1;
    margin: 18px;
  }
</style>