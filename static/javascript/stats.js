// Chart.js configuration
Chart.defaults.color = "#f3f4f6";
Chart.defaults.borderColor = "rgba(255, 255, 255, 0.1)";

// Function to generate random colors
function generateColors(count) {
  const colors = [
    "#2563eb",
    "#dc2626",
    "#059669",
    "#7c3aed",
    "#db2777",
    "#ea580c",
    "#ca8a04",
    "#2dd4bf",
    "#4f46e5",
    "#be123c",
  ];

  // If we need more colors than in our predefined array
  while (colors.length < count) {
    colors.push(colors[Math.floor(Math.random() * colors.length)]);
  }

  return colors.slice(0, count);
}

// Function to show error message in a chart container
function showChartError(containerId, message) {
  const container = document.getElementById(containerId);
  if (container) {
    container.style.height = "200px";
    container.style.display = "flex";
    container.style.alignItems = "center";
    container.style.justifyContent = "center";
    container.innerHTML = `<div class="text-muted">${message}</div>`;
  }
}

// Fetch monthly stats data
fetch("/expense_month_data/")
  .then((response) => response.json())
  .then((data) => {
    // Daily Trend Chart
    if (data.daily_amounts && data.daily_amounts.length > 0) {
      const dailyTrendCtx = document
        .getElementById("dailyTrendChart")
        .getContext("2d");
      new Chart(dailyTrendCtx, {
        type: "line",
        data: {
          labels: data.dates,
          datasets: [
            {
              label: "Daily Expenses",
              data: data.daily_amounts,
              borderColor: "#2563eb",
              backgroundColor: "rgba(37, 99, 235, 0.1)",
              borderWidth: 2,
              fill: true,
              tension: 0.4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              mode: "index",
              intersect: false,
              backgroundColor: "rgba(0, 0, 0, 0.8)",
              titleColor: "#fff",
              bodyColor: "#fff",
              borderColor: "#2d2d2d",
              borderWidth: 1,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: "rgba(255, 255, 255, 0.1)",
              },
            },
            x: {
              grid: {
                display: false,
              },
            },
          },
          interaction: {
            intersect: false,
            mode: "index",
          },
        },
      });
    } else {
      showChartError(
        "dailyTrendChart",
        "No expense data available for this month"
      );
    }

    // Category Distribution Chart
    if (data.categories && data.categories.length > 0) {
      const categoryCtx = document
        .getElementById("categoryChart")
        .getContext("2d");
      const colors = generateColors(data.categories.length);

      new Chart(categoryCtx, {
        type: "doughnut",
        data: {
          labels: data.categories,
          datasets: [
            {
              data: data.category_amounts,
              backgroundColor: colors,
              borderColor: "#1a1a1a",
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          layout: {
            padding: {
              left: 10,
              right: 10,
              top: 0,
              bottom: 0,
            },
          },
          plugins: {
            legend: {
              position: "right",
              align: "center",
              labels: {
                padding: 15,
                usePointStyle: true,
                pointStyle: "circle",
                font: {
                  size: 11,
                },
                boxWidth: 8,
              },
            },
            tooltip: {
              backgroundColor: "rgba(0, 0, 0, 0.8)",
              titleColor: "#fff",
              bodyColor: "#fff",
              borderColor: "#2d2d2d",
              borderWidth: 1,
              callbacks: {
                label: function (context) {
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const value = context.raw;
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `₹${value} (${percentage}%)`;
                },
              },
            },
          },
          cutout: "60%",
        },
      });
    } else {
      showChartError(
        "categoryChart",
        "No expense data available for this month"
      );
    }
  })
  .catch((error) => {
    console.error("Error fetching stats data:", error);
    showChartError("dailyTrendChart", "Error loading expense data");
    showChartError("categoryChart", "Error loading expense data");
  });
