<script lang="ts">
  import Chart from "chart.js/auto";
  import { onMount } from "svelte";
  import type { Hiscore, Player } from "../Types/types";
  export let hiscores: Hiscore[] = [];
  export let player: Player;

  let chartData = hiscores.map((hiscore: Hiscore) => hiscore.new_exp);
  let labels = hiscores.map((hiscore: Hiscore) =>
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
            label: "Total exp",
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
          tooltip: {
            callbacks: {
              label: function (context) {
                const tooltipLabels = [];

                let label = context.dataset.label || "";
                label += `: ${context.parsed.y.toLocaleString("en-US")}`;

                let gainedExpLabel = "From yesterday: +";
                context.dataIndex === 0
                  ? (gainedExpLabel += context.parsed.y - player.original_exp)
                  : (gainedExpLabel += (
                      context.parsed.y -
                      parseInt(
                        context.dataset.data[context.dataIndex - 1].toString()
                      )
                    ).toLocaleString("en-US"));

                let avgExpLabel = "Avg daily exp: ";
                let avgExp = Math.floor(
                  (parseInt(
                    context.dataset.data[context.dataIndex].toString()
                  ) -
                    player.original_exp) /
                    (context.dataIndex + 1)
                );
                avgExpLabel += avgExp.toLocaleString("en-US");

                tooltipLabels.push(label);
                tooltipLabels.push(gainedExpLabel);
                tooltipLabels.push(avgExpLabel);

                return tooltipLabels;
              },
            },
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
