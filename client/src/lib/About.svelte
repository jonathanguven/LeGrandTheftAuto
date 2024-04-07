<script>
  let project = {
    name: "LeGrandTheftAuto",
    url: "https://github.com/jonathanguven/LeGrandTheftAuto",
    data_url: "https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783/about_data"
  };
</script>

<svelte:head>
    <title>About</title>
</svelte:head>
<div class="flex flex-col items-center h-screen bg-base-200">
  <div class="text-4xl font-medium py-1">About</div>
    <a href={project.url} target="_blank" rel="noopener noreferrer" class="m-6">
        <svg xmlns="http://www.w3.org/2000/svg" width="3em" height="3em" viewBox="0 0 24 24" class="icon">
            <path
                    d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
            />
        </svg>
    </a>
    <a href="https://github.com/jonathanguven/" target="_blank" class="icon text-2xl pb-4">github.com/jonathanguven</a>
    <a href="https://github.com/jonathanguven/" target="_blank" class="icon text-2xl pb-4">github.com/maxhsieh08</a>

    <div class="about flex flex-col items-center mt-8 max-w-xl">
      <p class="pb-4">
        {project.name} is a project built by Jonathan Nguyen and Max Hsieh at SF Hacks 2024, 
        SFSU's premiere hackathon. However, Gurshan Warya left our group.
      </p>
      <p class="pb-4">
        We followed City Life Challenge Track 🏙, where hackers are encouraged 
        to find innovative ways to tackle issues faced everyday by urban communities like here in 
        San Francisco. We chose to tackle the issue of car theft and vehicle safety by creating an 
        interactive map displaying car-related incidents in San Francisco.
      </p>
      <p class="pb-4">
        This project was built using Vite+Svelte on the frontend, and Python+FastAPI on the backend.
        We used MapBoxGl to display the map and crime incident markers, and got our data from the San Francisco
        Police Department's publicly available data report shown <span><a href={project.data_url} class="underline">here</a></span>.
      </p>
    </div>
</div>

<style>
  .about {
      min-width: 300px;
      max-width: 60%;
      text-align: center;
  }
  
  .icon {
      transition: all 0.3s ease;
  }

  .icon:hover {
      transform: scale(1.1); 
  }
</style>