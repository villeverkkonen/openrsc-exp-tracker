<script lang="ts">
  import { onMount } from "svelte";

  let hiscores = []

  onMount(async () => {
    await getHiscores()
  });

  async function getHiscores() {
    let response = await fetch("/api/hiscores", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    let result = await response.json();
    hiscores = result;
  }
</script>

<main>
  <h1>OpenRSC Skilling Competition</h1>
  {#each hiscores as { playerName, oldExp, newExp, gainedExp }}
    <div class="playerCard">
      <p class="playerName">{playerName}</p>
      <div class="expContainer">
        <span class="exp">Old exp: {oldExp}</span>
        <span class="exp expGained">Gained: {gainedExp}</span>
        <span class="exp">New exp: {newExp}</span>
      </div>
    </div>
  {/each}
</main>

<style>
  .playerCard {
    background-color: black;
    padding: 3px;
    margin: 5px;
    border-radius: 5px;
  }

  .playerName {
    text-align: center;
  }

  .expContainer {
    display: flex;
    text-align: center;
  }

  .exp {
    padding-left: 10px;
    padding-right: 10px;
  }

  .expGained {
    color: red;
  }
</style>
