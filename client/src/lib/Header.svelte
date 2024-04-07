<script>
  import { Link } from "svelte-routing";
</script>

<div class="navbar bg-base-200 p-4">
  <div class="flex-1">
    <Link to="/" class="btn btn-ghost text-xl">LeGrandTheftAuto</Link>
  </div>
  <div class="flex-none">
    <div class="flex-1">
      <Link to="/about" class="btn btn-ghost text-lg">About</Link>
    </div>
  </div>
</div>