<script>
  import { Link } from "svelte-routing";
</script>

<div class="navbar bg-base-200 p-4">
  <div class="flex-1">
    <Link to="/" class="btn text-3xl btn-ghost">biip</Link>
  </div>
  <div class="flex-none">
    <div class="flex-1">
      <Link to="/about" class="btn text-xl btn-ghost">About</Link>
    </div>
  </div>
</div>