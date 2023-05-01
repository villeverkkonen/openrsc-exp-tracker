<script lang="ts">
  import axios from "axios";
  import { onMount } from "svelte";

  interface Player {
    id: number;
    name: string;
    original_exp: number;
    created_at: Date;
  }

  interface Hiscore {
    id: number;
    new_exp: number;
    created_at: Date;
    player_id: number;
  }

  interface MostEfficientDay {
    day: string;
    gained_exp: number;
  }

  interface HiscoresByPlayer {
    player: Player;
    hiscores: Hiscore[];
    most_efficient_day: MostEfficientDay;
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
          ...result.map(
            (hiscoreByPlayer) =>
              hiscoreByPlayer.hiscores[hiscoreByPlayer.hiscores.length - 1]
                .new_exp - hiscoreByPlayer.player.original_exp
          )
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
  <h3>OpenRSC gained overall experience tracker since May 5th 2023</h3>
  {#if loading}
    <p>Loading...</p>
  {:else}
    <div class="cardContainer">
      {#each hiscoresByPlayers as { player, hiscores, most_efficient_day }}
        <div class="card">
          <span class="playerName">{player.name}</span>
          <div class="expContainer">
            <span
              >{(
                Math.round(hiscores[hiscores.length - 1].new_exp * 100) / 100
              ).toLocaleString("en-US")} exp</span
            >
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
            <div>
              {#each hiscores as hiscore}
                <div>
                  {`${new Date(hiscore.created_at).toDateString()} - ${
                    hiscore.new_exp
                  } exp`}
                </div>
              {/each}
            </div>
            <div>
              <p>
                Most efficient day:
                {`${new Date(most_efficient_day.day).toDateString()} - ${
                  most_efficient_day.gained_exp
                } exp`}
              </p>
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
