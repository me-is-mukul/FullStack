// Draws the two charts on the "My reports" page with Chart.js.
// All numbers are calculated in reports/views.py and placed in the page
// by the json_script template filter. This file only draws them.

function readJson(id) {
  var element = document.getElementById(id);
  return element ? JSON.parse(element.textContent) : null;
}

var PURPLE = "#6f52c9";
var LIGHT_PURPLE = "#c9bdf0";

var xpData = readJson("xp-chart-data");
var xpCanvas = document.getElementById("xp-chart");
if (xpData && xpCanvas) {
  new Chart(xpCanvas, {
    type: "bar",
    data: {
      labels: xpData.labels,
      datasets: [{ label: "XP earned", data: xpData.values, backgroundColor: PURPLE }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { maxTicksLimit: 10 } },
        y: { beginAtZero: true, ticks: { precision: 0 } },
      },
    },
  });
}

var categoryData = readJson("category-chart-data");
var categoryCanvas = document.getElementById("category-chart");
if (categoryData && categoryCanvas) {
  new Chart(categoryCanvas, {
    type: "bar",
    data: {
      labels: categoryData.labels,
      datasets: [
        { label: "All quests", data: categoryData.total, backgroundColor: LIGHT_PURPLE },
        { label: "Completed", data: categoryData.completed, backgroundColor: PURPLE },
      ],
    },
    options: {
      maintainAspectRatio: false,
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
    },
  });
}
