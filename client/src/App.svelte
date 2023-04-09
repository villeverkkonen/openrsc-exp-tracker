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
      .finally(() => {});
  }
</script>

<main>
  <h5>OpenRSC gained overall experience tracker since 9.4.2023</h5>
  {#await getHiscores()}
    <p>Loading...</p>
  {:then}
    <div class="cardContainer">
      {#each hiscores as { playerName, gainedExp }}
        <div class="card">
          <h5>{playerName}</h5>
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
  {/await}
</main>

<style>
  h5 {
    text-align: center;
  }

  .cardContainer {
    text-align: center;
    width: 50%;
    margin: auto;
  }

  .card {
    background-color: rgb(101, 83, 59);
  }

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
