<script>
  import { Router, Link, Route } from "svelte-routing";
  import Header from "./lib/Header.svelte";
  import Home from "./lib/Home.svelte";
  import About from "./lib/About.svelte";

  export let url = "";
</script>

<Router {url}>
  <Header />
  <div>
    <Route path="/" component={Home} />
    <Route path="/about" component={About} />
  </div>
</Router>


