<script lang="ts">
  import axios from "axios";
  import { onMount } from "svelte";
  import LineChart from "./components/LineChart.svelte";

  interface Player {
    id: number;
    name: string;
    original_exp: number;
    created_at: Date;
  }

  interface Hiscore {
    id: number;
    new_exp: number;
    total_gained_exp: number;
    created_at: Date;
    player_id: number;
  }

  interface HiscoresByPlayer {
    player: Player;
    hiscores: Hiscore[];
  }

  let hiscoresByPlayers: HiscoresByPlayer[] = [];
  let highestExpGain: number = 0;
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
        highestExpGain = Math.max(
          ...result.map((hiscoreByPlayer) => {
            if (hiscoreByPlayer.hiscores.length === 0) {
              return 0;
            }
            return (
              hiscoreByPlayer.hiscores[hiscoreByPlayer.hiscores.length - 1]
                .new_exp - hiscoreByPlayer.player.original_exp
            );
          })
        );
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
          <div class="expContainer">
            {#if hiscores.length > 0}
              <p>
                Gained exp since {new Date(
                  hiscores[0].created_at
                ).toLocaleDateString("en-US")}: {(
                  Math.round(
                    hiscores[hiscores.length - 1].total_gained_exp * 100
                  ) / 100
                ).toLocaleString("en-US")}
              </p>
              <p>
                Total exp: {(
                  Math.round(hiscores[hiscores.length - 1].new_exp * 100) / 100
                ).toLocaleString("en-US")}
              </p>
              <div class="expBarContainer">
                <div
                  class="expBar"
                  style="width:{highestExpGain === 0
                    ? 0
                    : (100 *
                        (hiscores[hiscores.length - 1].new_exp -
                          player.original_exp)) /
                      highestExpGain}%"
                />
              </div>
              <LineChart data={hiscores} />
            {:else}
              <p>No data to show</p>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
  <a
    class="githubLink"
    href="https://github.com/villeverkkonen/openrsc-exp-tracker"
    target="_blank"
  >
    <img
      class="githubIcon"
      src="images/github-mark-white.svg"
      alt="Link to source code in GitHub"
    />
  </a>
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

  .expBarContainer {
    background-color: rgb(112 128 144);
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

  .githubLink {
    float: right;
    margin: 15px;
  }

  .githubIcon {
    width: 40px;
  }
</style>
