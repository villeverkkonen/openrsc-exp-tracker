<script lang="ts">
  import { onMount } from 'svelte';

  let hiscores = ''

  onMount(async() => {
    await getHiscores();
  })

  async function getHiscores() {
    let response = await fetch('/api/hiscores', {
      method: 'GET',
    })

    let result = await response.text()
    console.log(result)
    hiscores = result
  }
</script>

<main>
  <h1>OpenRSC Skilling Competition</h1>
  <p>Agility exp: {hiscores}</p>
</main>

<style>

</style>
