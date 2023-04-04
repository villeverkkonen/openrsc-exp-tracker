<script lang="ts">
  import { onMount } from 'svelte';

  let hiscores = []

  onMount(async() => {
    await getHiscores();
  })

  async function getHiscores() {
    let response = await fetch('/api/hiscores', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    let result = await response.json()
    console.log(result)
    hiscores = result
  }
</script>

<main>
  <h1>OpenRSC Skilling Competition</h1>
  {#each hiscores as { playerName, oldExp, newExp }}
    <div>
      <p>Player: {playerName}</p>
      <p>Old exp: {oldExp}</p>
      <p>New exp: {newExp}</p>
    </div>
  {/each}
</main>

<style>

</style>
