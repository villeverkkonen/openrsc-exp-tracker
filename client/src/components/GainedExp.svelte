<script lang="ts">
  import type { Hiscore } from "../Types/types";
  export let hiscores: Hiscore[] = [];
</script>

<main>
  <p>
    Gained exp since {new Date(hiscores[0].created_at).toLocaleDateString(
      "en-US"
    )}: {Math.floor(
      hiscores[hiscores.length - 1].total_gained_exp
    ).toLocaleString("en-US")}
  </p>
</main>
