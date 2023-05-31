<script lang="ts">
  import type { Hiscore, Player } from "../Types/types";
  import AverageDailyExp from "./AverageDailyExp.svelte";
  import GainedExp from "./GainedExp.svelte";
  import LineChart from "./LineChart.svelte";
  import TotalExp from "./TotalExp.svelte";
  export let player: Player;
  export let hiscores: Hiscore[] = [];
</script>

<main>
  <div>
    {#if hiscores.length > 0}
      <GainedExp {hiscores} />
      <TotalExp newExp={hiscores[hiscores.length - 1].new_exp} />
      <AverageDailyExp {hiscores} />
      <LineChart {player} {hiscores} />
    {:else}
      <p>No data to show</p>
    {/if}
  </div>
</main>
