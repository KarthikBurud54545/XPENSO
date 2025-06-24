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

  while (colors.length < count) {
    colors.push(colors[Math.floor(Math.random() * colors.length)]);
  }

  return colors.slice(0, count);
}

let expenseChart = null;
let currentChartType = "bar";

// Function to create or update the expense chart
function updateExpenseChart(data, type) {
  try {
    console.log("Updating chart with data:", data);
    const ctx = document.getElementById("expenseChart");
    if (!ctx) {
      console.error("Could not find expense chart canvas");
      return;
    }

    // Ensure we have the expense category data
    if (!data || !data.expense_category_data) {
      console.error("Invalid data format:", data);
      return;
    }

    const categories = Object.keys(data.expense_category_data);
    const amounts = Object.values(data.expense_category_data);
    const colors = generateColors(categories.length);

    const config = {
      type: type,
      data: {
        labels: categories,
        datasets: [
          {
            label: "Yearly Expenses",
            data: amounts,
            backgroundColor: colors,
            borderColor: type === "bar" ? colors : "#1a1a1a",
            borderWidth: type === "bar" ? 0 : 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: type === "pie" ? "right" : "top",
            labels: {
              color: "#f3f4f6",
              usePointStyle: type === "pie",
              padding: type === "pie" ? 15 : 10,
            },
          },
          tooltip: {
            backgroundColor: "rgba(0, 0, 0, 0.8)",
            titleColor: "#fff",
            bodyColor: "#fff",
            callbacks: {
              label: function (context) {
                const value = context.raw;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `₹${value.toLocaleString()} (${percentage}%)`;
              },
            },
          },
        },
        scales:
          type === "bar"
            ? {
                y: {
                  beginAtZero: true,
                  grid: {
                    color: "rgba(255, 255, 255, 0.1)",
                  },
                  ticks: {
                    callback: function (value) {
                      return "₹" + value.toLocaleString();
                    },
                  },
                },
                x: {
                  grid: {
                    display: false,
                  },
                },
              }
            : undefined,
      },
    };

    if (expenseChart) {
      expenseChart.destroy();
    }
    expenseChart = new Chart(ctx, config);
    console.log("Chart updated successfully");
  } catch (error) {
    console.error("Error updating chart:", error);
  }
}

// Function to create the trend chart
function createTrendChart(data) {
  const ctx = document.getElementById("trendChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: data.months,
      datasets: [
        {
          label: "Income",
          data: data.income_trend,
          borderColor: "#059669",
          backgroundColor: "rgba(5, 150, 105, 0.1)",
          fill: true,
          tension: 0.4,
        },
        {
          label: "Expenses",
          data: data.expense_trend,
          borderColor: "#dc2626",
          backgroundColor: "rgba(220, 38, 38, 0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: "index",
      },
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          titleColor: "#fff",
          bodyColor: "#fff",
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
    },
  });
}

// Function to toggle chart type
function toggleChartType(type) {
  if (type !== currentChartType) {
    currentChartType = type;
    fetch("/info_year/")
      .then((response) => response.json())
      .then((data) => {
        updateExpenseChart(data, type);
      })
      .catch((error) => {
        console.error("Error fetching expense data:", error);
      });
  }
}

// Initial data fetch and chart creation
document.addEventListener("DOMContentLoaded", function () {
  fetch("/info_year/")
    .then((response) => response.json())
    .then((data) => {
      updateExpenseChart(data, currentChartType);
    })
    .catch((error) => {
      console.error("Error fetching expense data:", error);
    });
});

// Fetch monthly trend data
fetch("/monthly_trend/")
  .then((response) => response.json())
  .then((data) => {
    createTrendChart(data);
  })
  .catch((error) => {
    console.error("Error fetching trend data:", error);
  });
