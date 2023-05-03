import { DynamicFilter, onChangeSelect } from "./dynamic.js";

const form = document.getElementById("filter-trucks-form");

// Home Cards
const counter = document.getElementById("data-counter");
const counterContainer = document.getElementById("data-counter-container");
const average = document.getElementById("data-average");
const averageContainer = document.getElementById("data-average-container");
const detailsToggle = document.getElementById("details-toggle");
const filterContainer = document.getElementById("filter-container");
const tableContainer = document.getElementById("table-container");
const headingContainer = document.getElementById("heading-container");
const topCardsContainer = document.getElementById("top-cards-container");

// Details Cards
const filteredVehiclesCounterContainer = document.getElementById("filtered-vehicles-counter-container");
const filteredVehiclesCounter = document.getElementById("filtered-vehicles-counter");
const filteredVehiclesAverageContainer = document.getElementById("filtered-vehicles-average-container");
const filteredVehiclesAverage = document.getElementById("filtered-vehicles-average");
const filteredVehiclesToggle = document.getElementById("filtered-vehicles-toggle");

// Dynamic Filters
var filter = new DynamicFilter();
const resetButton = document.getElementById("reset-filters-button");

resetButton.addEventListener('click', function() {
	filter.resetFilters();
});

// Form Selects
form.onchange = onChangeSelect;
form.filter = filter;

window.filteredVehiclesData = [];

form.addEventListener("submit", function (e) {
  e.preventDefault();

  let values = {};
  const entry = Object.fromEntries(new FormData(e.target));
  for (const [key, value] of Object.entries(entry)) {
    if (value.length > 0) values[key] = value;
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
      window.filteredVehiclesData = data;
    })
    .catch(console.error);
});

detailsToggle.addEventListener("click", function () {
  filterContainer.style.display = "none";
  tableContainer.style.display = "";

  createTable();

  headingContainer.style.display = "none";
  topCardsContainer.style.display = "";

  topCardsContainer.style.display = "";
  filteredVehiclesToggle.style.display = "";
  filteredVehiclesCounterContainer.style.display = "";
  filteredVehiclesAverageContainer.style.display = "";
  filteredVehiclesAverage.innerHTML = "$" + calculateAverage(window.filteredVehiclesData).toFixed(2);
  filteredVehiclesCounter.innerHTML = window.filteredVehiclesData.length;
});

filteredVehiclesToggle.addEventListener("click", function() {
  filterContainer.style.display = "";
  tableContainer.style.display = "none";

  headingContainer.style.display = "";
  topCardsContainer.style.display = "none";

  topCardsContainer.style.display = "none";
  filteredVehiclesToggle.style.display = "none";
  filteredVehiclesCounterContainer.style.display = "none";
  filteredVehiclesAverageContainer.style.display = "none";
});

function calculateAverage(data) {
  return (
    data.reduce((total, current) => total + parseFloat(current.saleprice), 0) /
    data.length
  );
}

function createTable() {
  const rowClass = "border-b border-gray-100 dark:border-gray-700/50";
  const cellClass = "p-3 text-lg text-center";
  const pClass = "text-black-100 dark:text-black-200";
  const tableBody = document.getElementById("data-table-body");
  const tableHeadingRow = document.getElementById("data-table-heading-row");

  const headers = Object.keys(window.filteredVehiclesData[0]);

  // Create headers
  for (let i = 0; i < headers.length; i++) {
    const heading = document.createElement("th");
    heading.className = "px-3 py-4 text-gray-900 bg-gray-100/75 font-semibold text-left text-2xl dark:text-gray-50 dark:bg-gray-700/25";
    heading.innerHTML = parseHeaderName(headers[i]);
    tableHeadingRow.appendChild(heading);
  }

  // Fill body with data
  window.filteredVehiclesData.forEach((item) => {
    const values = Object.values(item);
    const row = document.createElement("tr");
    row.className = rowClass;

    for (let i = 0; i < values.length; i++) {
      const cell = document.createElement("td");
      cell.className = cellClass;

      const p = document.createElement("p");
      p.className = pClass;
      p.innerHTML = values[i];
      cell.appendChild(p);

      row.appendChild(cell);
    }

    tableBody.appendChild(row);
  });
}

function parseHeaderName(header) {
  let headers = {
    id: "ID",
    sale_date: "Sale Date",
    vin: "VIN",
    saledocumenttype: "Sale Document Type",
    loss_type: "Loss Type",
    damage_description_primary: "Damage Description Primary",
    starts_at_checkin: "Starts At Check-In",
    runs_and_drives: "Runs & Drives",
    miles: "Miles",
    offer: "Offer",
    odometerreadingtypedescription: "Odometer Reading Type Descr.",
    air_bags_deployed: "Air Bags Deployed",
    saleprice: "Sale Price",
    branch: "Branch",
    branch_zip_code: "Branch Zip COde",
    drivelinetype: "DriveLine Type",
    year: "Year",
    make: "Make",
    model: "Model",
    trim: "Trim",
    bodytype: "Body Type",
    cabtype: "Cab Type",
    fueltype: "Fuel Type",
    enginesize: "Engine Size",
    data_type: "Data Type",
    stateabbreviation: "State Abbreviation",
  };
  return headers[header];
}
