<script>
  import Chart from "chart.js/auto";
  import { onMount } from "svelte";
  export let data;

  let chartData = data.map((hiscore) => hiscore.new_exp);
  let labels = data.map((hiscore) =>
    new Date(hiscore.created_at).toLocaleDateString("en-US")
  );
  let ctx;
  let chartCanvas;

  onMount(async () => {
    ctx = chartCanvas.getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Exp",
            data: chartData,
            borderColor: "cyan",
          },
        ],
      },
      options: {
        animation: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: {
              color: "#e8d800",
            },
          },
          y: {
            ticks: {
              color: "#e8d800",
            },
          },
        },
      },
    });
  });
</script>

<canvas bind:this={chartCanvas} id="expChart" />
