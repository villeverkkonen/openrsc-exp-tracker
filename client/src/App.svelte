<script lang="ts">
  import axios from "axios";
  import { onMount } from "svelte";

  interface Hiscore {
    playerName: string;
    oldExp: number;
    newExp: number;
    gainedExp: number;
  }

  let hiscores: Hiscore[] = [];
  let highestExpGain: number = 0;
  let loading: boolean = true;

  onMount(async () => {
    await getHiscores();
  });

  async function getHiscores() {
    await axios
      .get("/api/hiscores")
      .then((response) => {
        let result: Hiscore[] = response.data;

        hiscores = result;
        highestExpGain = Math.max(
          ...result.map((hiscore) => hiscore.gainedExp)
        );
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        loading = false;
      });
  }
</script>

<main>
  <h3>OpenRSC gained overall experience tracker since 10.4.2023</h3>
  {#if loading}
    <p>Loading...</p>
  {:else}
    <div class="cardContainer">
      {#each hiscores as { playerName, gainedExp }}
        <div class="card">
          <span class="playerName">{playerName}</span>
          <div class="expContainer">
            <span>{Math.round(gainedExp * 100) / 100} exp</span>
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
  {/if}
</main>

<style>
  :global(html) {
    background-color: black;
  }

  h3 {
    text-align: center;
    color: rgb(255 165 0);
  }

  .cardContainer {
    text-align: center;
    width: 50%;
    max-width: 25rem;
    margin: 5px auto;
  }

  .card {
    background-color: rgb(65 105 225);
    color: rgb(255 165 0);
    padding: 5px;
    margin: 10px;
    border-radius: 10px;
  }

  .playerName {
    font-weight: bold;
  }

  .expBarContainer {
    background-color: rgb(119 136 153);
    height: 24px;
    width: 90%;
    padding: 4px;
    border-radius: 3px;
    margin: 5px auto;
  }

  .expBar {
    background-color: cyan;
    height: 100%;
  }
</style>
