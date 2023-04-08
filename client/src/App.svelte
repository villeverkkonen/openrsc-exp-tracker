<script lang="ts">
  import { onMount } from "svelte";

  interface Hiscore {
    playerName: string;
    oldExp: number;
    newExp: number;
    gainedExp: number;
  }

  let hiscores: Hiscore[] = [];
  let highestExpGain: number = 0;

  onMount(async () => {
    await getHiscores();
  });

  async function getHiscores() {
    let response = await fetch("/api/hiscores", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    let result: Hiscore[] = await response.json();
    hiscores = result;
    highestExpGain = Math.max(...result.map((hiscore) => hiscore.gainedExp));
  }
</script>

<main>
  <h1>
    OpenRSC gained overall experience tracker since 8.4.2023
  </h1>
  <div>
    {#each hiscores as { playerName, gainedExp }}
      <div>
        <h5>{playerName}</h5>
        <div class="expContainer">
          <span>{(Math.round(gainedExp * 100) / 100).toFixed(2)} exp</span>
          <div class="expBarContainer">
            <div
              class="expBar"
              style="width:{highestExpGain === 0
                ? 0
                : (100 * gainedExp) / highestExpGain}%"
            />
          </div>
        </div>
      </div>
    {/each}
  </div>
</main>

<style>
  .expBarContainer {
    background-color: rgb(179, 188, 203);
    height: 24px;
    width: 100%;
    padding: 4px;
    border-radius: 3px;
    margin: 5px 0 5px 0;
  }

  .expBar {
    background-color: cyan;
    height: 100%;
  }
</style>
