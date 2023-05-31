<script lang="ts">
  import type { Hiscore } from "../Types/types";
  export let hiscores: Hiscore[] = [];
</script>

<main>
  <p>
    Average daily exp: {Math.floor(
      hiscores[hiscores.length - 1].total_gained_exp / hiscores.length
    ).toLocaleString("en-US")}
  </p>
</main>
