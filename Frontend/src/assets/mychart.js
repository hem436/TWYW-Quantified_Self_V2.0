/* eslint-disable */
let config={
  type: "line",
  data: {
    // labels: xlabel,
    datasets: [
      {
        label: "# val",
        // data: ylabel,
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)"
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)"
        ],
        borderWidth: 1
      }
    ]
  },
  options: {
    scales: {
      x: {
        type: "time",
        time: {
          unit: "minute"
          // displayFormats: {
          //       minute: 'HH:MM'
          //   },
        },
        ticks: {
          maxRotation: 0,
          major: {
            enabled: true
          }
        }
      },
      y: {
        beginAtZero: true
      }
    }
  }}
export default config;
