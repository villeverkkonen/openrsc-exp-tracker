<script lang="ts">
  import axios from "axios";
  import { onMount } from "svelte";
  import type { HiscoresByPlayer } from "./Types/types";
  import ExpContainer from "./components/ExpContainer.svelte";

  let hiscoresByPlayers: HiscoresByPlayer[] = [];
  let loading: boolean = true;

  onMount(async () => {
    await getHiscores();
  });

  const getHiscores = async () => {
    await axios
      .get("/api/hiscores_by_players")
      .then((response) => {
        const result: HiscoresByPlayer[] = response.data;
        hiscoresByPlayers = result;
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        loading = false;
      });
  };
</script>

<main>
  <h3>OpenRSC overall experience tracker</h3>
  {#if loading}
    <p>Loading...</p>
  {:else}
    <div class="cardContainer">
      {#each hiscoresByPlayers as { player, hiscores }}
        <div class="card">
          <span class="playerName">{player.name}</span>
          <ExpContainer {player} {hiscores} />
        </div>
      {/each}
    </div>
  {/if}
</main>

<style>
  :global(html) {
    background-color: #121212;
  }

  h3 {
    text-align: center;
    color: #e8d800;
  }

  .cardContainer {
    text-align: center;
    width: 80%;
    max-width: 25rem;
    margin: 5px auto;
  }

  .card {
    background-color: #1e1e1e;
    box-shadow: 4px 8px black;
    color: #e8d800;
    padding: 5px;
    margin: 15px;
    border-radius: 5px;
  }

  .playerName {
    font-weight: bold;
  }
</style>
