<script>
  import Chart from "chart.js/auto";
  import { onMount } from "svelte";
  export let data;

  let chartData = data.map((hiscore) => hiscore.new_exp);
  let labels = data.map((hiscore) =>
    new Date(hiscore.created_at).toDateString()
  );
  let ctx;
  let chartCanvas;

  onMount(async (promise) => {
    ctx = chartCanvas.getContext("2d");
    var chart = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Exp",
            data: chartData,
          },
        ],
      },
      options: {
        animation: false,
      },
    });
  });
</script>

<canvas bind:this={chartCanvas} id="myChart" />