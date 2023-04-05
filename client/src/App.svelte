<script lang="ts">
  import { onMount } from "svelte";
  import { Card } from "flowbite-svelte";

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
  <!-- <h1 class="my-5 text-center">OpenRSC gained overall experience tracker</h1> -->
  <div>
    {#each hiscores as { playerName, gainedExp }}
      <Card
        class="my-5 m-auto items-center mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
      >
        <h5>{playerName}</h5>
        <div class="expContainer">
          <span
            class="font-normal text-gray-700 dark:text-gray-400 leading-tight"
            >{(Math.round(gainedExp * 100) / 100).toFixed(2)} exp</span
          >
          <div class="expBarContainer">
            <div
              class="expBar"
              style="width:{highestExpGain === 0
                ? 0
                : (100 * gainedExp) / highestExpGain}%"
            />
          </div>
        </div>
      </Card>
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
