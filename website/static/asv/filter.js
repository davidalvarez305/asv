const form = document.getElementById("filter-trucks-form");
const counter = document.getElementById("data-counter");
const counterContainer = document.getElementById("data-counter-container");
const average = document.getElementById("data-average");
const averageContainer = document.getElementById("data-average-container");
const detailsToggle = document.getElementById("details-toggle");
const filterContainer = document.getElementById("filter-container");
const tableContainer = document.getElementById("table-container");

window.apiData = [];

form.addEventListener("submit", function (e) {
  e.preventDefault();

  let values = {};
  const entry = Object.fromEntries(new FormData(e.target));
  for (const [key, value] of Object.entries(entry)) {
    if (value.length > 0) values[key] = value.toUpperCase();
  }
  const data = new URLSearchParams(values);

  fetch("/trucks?" + data.toString(), {
    headers: {
      "Content-Type": "application/json",
    },
    method: "GET",
    credentials: "include",
  })
    .then((response) => response.json())
    .then(({ data }) => {
      counterContainer.style.display = "";
      counter.innerHTML = data.length;
      averageContainer.style.display = "";
      average.innerHTML = "$" + calculateAverage(data).toFixed(2);
      detailsToggle.style.display = "";
      apiData = data;
    })
    .catch(console.error);
});

detailsToggle.addEventListener("click", function() {
  filterContainer.style.display = "none";
  tableContainer.style.display = "";

  createTable();
});

function calculateAverage(data) {
  return data.reduce((total, current) => total + parseFloat(current.saleprice), 0) / data.length;
}

function createTable() {
  const rowClass = "border-b border-gray-100 dark:border-gray-700/50";
  const cellClass = "p-3";
  const pClass = "text-gray-500 dark:text-black-200";
  const tableBody = document.getElementById("data-table-body");
  const tableHeadingRow = document.getElementById("data-table-heading-row");

  const headers = Object.keys(window.apiData[0]);

  // Create headers
  for (let i = 0; i < headers.length; i++) {
    const heading = document.createElement('th');
    heading.className = "px-3 py-4 text-gray-900 bg-gray-100/75 font-semibold text-left dark:text-gray-50 dark:bg-gray-700/25";
    heading.innerHTML = headers[i];
    tableHeadingRow.appendChild(heading);
  }

  // Fill body with data
  window.apiData.forEach((item) => {
    const values = Object.values(item);
    const row = document.createElement('tr');
    row.className = rowClass;

    for (let i = 0; i < values.length; i++) {
      const cell = document.createElement('td');
      cell.className = cellClass;
      
      const p = document.createElement('p');
      p.className = pClass;
      p.innerHTML = values[i];
      cell.appendChild(p);

      row.appendChild(cell);
    };

    tableBody.appendChild(row);
  });
}
