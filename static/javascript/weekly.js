// Chart.js configuration
Chart.defaults.set("responsive", true);
Chart.defaults.set("maintainAspectRatio", false);
Chart.defaults.set("color", "#f3f4f6");
Chart.defaults.set("borderColor", "rgba(255, 255, 255, 0.1)");
Chart.defaults.set(
  "font.family",
  "'Inter', 'system-ui', '-apple-system', 'sans-serif'"
);

// Color palette for charts
const chartColors = [
  "#3b82f6",
  "#ef4444",
  "#10b981",
  "#f59e0b",
  "#6366f1",
  "#ec4899",
  "#8b5cf6",
  "#14b8a6",
  "#f97316",
  "#06b6d4",
];

// Modern pastel color palette
const pastelColors = [
  "#7dd3fc",
  "#fca5a5",
  "#a7f3d0",
  "#fde68a",
  "#c4b5fd",
  "#f9a8d4",
  "#fcd34d",
  "#6ee7b7",
  "#fbbf24",
  "#93c5fd",
];

// Chart.js shadow plugin
Chart.register({
  id: "customShadow",
  beforeDatasetsDraw: (chart) => {
    const ctx = chart.ctx;
    ctx.save();
    ctx.shadowColor = "rgba(54,162,235,0.18)";
    ctx.shadowBlur = 18;
  },
  afterDatasetsDraw: (chart) => {
    chart.ctx.restore();
  },
});

// Simple debug function
function debug(message, data) {
  console.log(message, data);
  const debugOutput = document.getElementById("debugOutput");
  if (debugOutput) {
    debugOutput.innerHTML += `<br>${message}: ${JSON.stringify(data)}`;
  }
}

// Get chart data from the template
const chartData = JSON.parse(document.getElementById("chart-data").textContent);

// Debug output
console.log("DOM loaded, initializing chart...");
console.log("Chart Data:", chartData);

let weeklyChart;

// Set default Chart.js options for dark theme
Chart.defaults.color = "#f3f4f6";
Chart.defaults.borderColor = "rgba(255, 255, 255, 0.1)";

// Helper: Create a gradient for each pie slice
function createPieGradients(ctx, count) {
  const gradients = [];
  const colorPairs = [
    ["#7dd3fc", "#2563eb"],
    ["#fca5a5", "#ef4444"],
    ["#a7f3d0", "#10b981"],
    ["#fde68a", "#f59e0b"],
    ["#c4b5fd", "#6366f1"],
    ["#f9a8d4", "#ec4899"],
    ["#fcd34d", "#fbbf24"],
    ["#6ee7b7", "#14b8a6"],
    ["#fbbf24", "#f59e0b"],
    ["#93c5fd", "#3b82f6"],
  ];
  for (let i = 0; i < count; i++) {
    const grad = ctx.createLinearGradient(0, 0, 300, 300);
    grad.addColorStop(0, colorPairs[i % colorPairs.length][0]);
    grad.addColorStop(1, colorPairs[i % colorPairs.length][1]);
    gradients.push(grad);
  }
  return gradients;
}

// Helper: Animate center label count-up
function animateCenterLabel(chart, targetValue) {
  let current = 0;
  const duration = 1200;
  const start = performance.now();
  function animate(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    current = Math.floor(progress * targetValue);
    chart._centerLabelValue = current;
    chart.draw();
    if (progress < 1) requestAnimationFrame(animate);
    else {
      chart._centerLabelValue = targetValue;
      chart.draw();
    }
  }
  requestAnimationFrame(animate);
}

function createDoughnutCenterLabel(chart, label) {
  const ctx = chart.ctx;
  ctx.save();
  ctx.font = "bold 1.5rem Inter, sans-serif";
  ctx.fillStyle = "#fff";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.shadowColor = "#2563eb";
  ctx.shadowBlur = 16;
  ctx.fillText(label, chart.width / 2, chart.height / 2);
  ctx.restore();
}

function initializeWeeklyChart(type = "bar") {
  const ctx = document.getElementById("weeklyChart").getContext("2d");
  let backgroundColor, borderColor, cutout, afterDraw;
  if (type === "bar") {
    backgroundColor = ctx.createLinearGradient(0, 0, 0, 400);
    backgroundColor.addColorStop(0, "#2563eb");
    backgroundColor.addColorStop(0.5, "#60a5fa");
    backgroundColor.addColorStop(1, "#a7f3d0");
    borderColor = "#2563eb";
    cutout = undefined;
    afterDraw = undefined;
  } else {
    backgroundColor = createPieGradients(ctx, chartData.categories.length);
    borderColor = backgroundColor;
    cutout = "70%";
    afterDraw = (chart) => {
      const total = chartData.categories.reduce(
        (sum, cat) => sum + cat.amount,
        0
      );
      if (typeof chart._centerLabelValue === "undefined") {
        chart._centerLabelValue = 0;
        animateCenterLabel(chart, total);
      }
      createDoughnutCenterLabel(
        chart,
        "₹" + (chart._centerLabelValue || 0).toLocaleString("en-IN")
      );
    };
  }
  const labels =
    type === "bar"
      ? Object.keys(chartData.dailySpending)
      : chartData.categories.map((cat) => cat.name);
  const data =
    type === "bar"
      ? Object.values(chartData.dailySpending)
      : chartData.categories.map((cat) => cat.amount);
  if (weeklyChart) weeklyChart.destroy();
  weeklyChart = new Chart(ctx, {
    type: type === "pie" ? "doughnut" : "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: type === "bar" ? "Daily Spending" : "Category Breakdown",
          data: data,
          backgroundColor: backgroundColor,
          borderColor: borderColor,
          borderWidth: type === "pie" ? (ctx) => (ctx.active ? 8 : 3) : 2,
          borderRadius: type === "bar" ? 22 : 0,
          borderSkipped: false,
          hoverOffset: type === "pie" ? (ctx) => (ctx.active ? 28 : 0) : 8,
          offset: type === "pie" ? (ctx) => (ctx.active ? 22 : 0) : 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: cutout,
      animation: {
        duration: 1800,
        easing: "easeOutBack",
        animateScale: true,
        animateRotate: true,
      },
      plugins: {
        legend: {
          display: false, // We'll render a custom legend below
        },
        tooltip: {
          backgroundColor: "rgba(37,99,235,0.97)",
          titleColor: "#fff",
          bodyColor: "#fff",
          padding: 16,
          displayColors: true,
          borderColor: "rgba(255, 255, 255, 0.18)",
          borderWidth: 1,
          caretSize: 8,
          caretPadding: 8,
          cornerRadius: 10,
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || "";
              if (label) label += ": ";
              label += new Intl.NumberFormat("en-IN", {
                style: "currency",
                currency: "INR",
                maximumFractionDigits: 0,
              }).format(context.parsed.y || context.parsed);
              return label;
            },
          },
        },
        customShadow: {},
      },
      scales: {
        y: {
          display: type === "bar",
          beginAtZero: true,
          grid: {
            color: "rgba(255, 255, 255, 0.03)",
            drawBorder: false,
          },
          ticks: {
            color: "#9ca3af",
            padding: 10,
            font: { size: 13 },
            callback: function (value) {
              return "₹" + value.toLocaleString("en-IN");
            },
          },
        },
        x: {
          display: type === "bar",
          grid: { display: false },
          ticks: {
            color: "#9ca3af",
            padding: 10,
            font: { size: 13 },
          },
        },
      },
      onHover: (event, chartElement) => {
        if (weeklyChart && weeklyChart.config.type === "doughnut") {
          if (chartElement.length) {
            weeklyChart.setActiveElements(chartElement);
          } else {
            weeklyChart.setActiveElements([]);
          }
          weeklyChart.update();
        }
      },
      plugins: ["customShadow"],
      afterDraw: afterDraw,
    },
    plugins: ["customShadow"],
  });

  // Render custom legend below the chart for doughnut
  if (type === "pie") {
    const legendContainer = document.getElementById("custom-legend");
    if (legendContainer) {
      legendContainer.innerHTML = chartData.categories
        .map(
          (cat, idx) => `
        <span class="legend-pill" style="background:${
          pastelColors[idx % pastelColors.length]
        }"></span>
        <span class="legend-label">${cat.name}</span>
      `
        )
        .join("<br>");
    }
  }
}

// Initialize chart when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded, initializing chart...");
  initializeWeeklyChart("bar");
});

// Add event listeners for chart type toggle buttons
document.getElementById("barChartBtn").addEventListener("click", () => {
  document.getElementById("barChartBtn").classList.add("bg-blue-700");
  document.getElementById("pieChartBtn").classList.remove("bg-blue-700");
  initializeWeeklyChart("bar");
});
document.getElementById("pieChartBtn").addEventListener("click", () => {
  document.getElementById("pieChartBtn").classList.add("bg-blue-700");
  document.getElementById("barChartBtn").classList.remove("bg-blue-700");
  initializeWeeklyChart("pie");
});

// Get Net Savings data from the script tag
const netSavingsScript = document.getElementById("net-savings-data");
const netSavings = JSON.parse(netSavingsScript.textContent || "0");

console.log("Net Savings value:", netSavings);

// Get the canvas element for Net Savings chart
const netSavingsCtx = document
  .getElementById("netSavingsChart")
  .getContext("2d");

// Register the data labels plugin
Chart.register(ChartDataLabels);

// Create the Net Savings bar chart
new Chart(netSavingsCtx, {
  type: "bar",
  data: {
    labels: ["Net Savings"],
    datasets: [
      {
        label: "Net Savings",
        data: [netSavings],
        backgroundColor: netSavings >= 0 ? "#4ade80" : "#f87171", // Green for positive, Red for negative
        borderColor: netSavings >= 0 ? "#4ade80" : "#f87171",
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false, // No legend needed for a single bar
      },
      title: {
        display: true,
        text: "Net Savings",
        color: "#f3f4f6",
      },
      datalabels: {
        anchor: "end",
        align: "top",
        color: netSavings >= 0 ? "#4ade80" : "#f87171", // Color based on value
        formatter: function (value) {
          return "₹" + value.toFixed(2);
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        min: netSavings < 0 ? netSavings * 1.1 : 0,
        ticks: {
          color: "#f3f4f6",
        },
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
      },
      x: {
        ticks: {
          color: "#f3f4f6",
        },
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
      },
    },
  },
});
