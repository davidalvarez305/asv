import { DynamicFilter } from "./dynamic.js";

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
const filteredVehiclesCounterContainer = document.getElementById(
  "filtered-vehicles-counter-container"
);
const filteredVehiclesCounter = document.getElementById(
  "filtered-vehicles-counter"
);
const filteredVehiclesAverageContainer = document.getElementById(
  "filtered-vehicles-average-container"
);
const filteredVehiclesAverage = document.getElementById(
  "filtered-vehicles-average"
);
const filteredVehiclesToggle = document.getElementById(
  "filtered-vehicles-toggle"
);

// Dynamic Filters
var filter = new DynamicFilter();
const resetButton = document.getElementById("reset-filters-button");

resetButton.addEventListener("click", function () {
  filter.resetFilters();
});

async function onChangeSelect(e) {
  let values = {};
  const entry = Object.fromEntries(new FormData(this));
  for (const [key, value] of Object.entries(entry)) {
    if (value.length > 0) values[key] = value;
  }
  const params = new URLSearchParams(values);

  try {
    const response = await fetch("/trucks?" + params.toString(), {
      headers: {
        "Content-Type": "application/json",
      },
      method: "GET",
      credentials: "include",
    });
    const { data } = await response.json();
    handleDisplayChangedData(data);
    this.filter.changeFilters(data);
  } catch (err) {
    console.error(err);
  }
}

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
    .then(({ data }) => handleDisplayChangedData(data))
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
  filteredVehiclesAverage.innerHTML =
    "$" + calculateAverage(window.filteredVehiclesData).toFixed(2);
  filteredVehiclesCounter.innerHTML = window.filteredVehiclesData.length;
});

filteredVehiclesToggle.addEventListener("click", function () {
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
    heading.className =
      "px-3 py-4 text-gray-900 bg-gray-100/75 font-semibold text-left text-2xl dark:text-gray-50 dark:bg-gray-700/25";
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

function handleDisplayChangedData(data) {
  counterContainer.style.display = "";
  counter.innerHTML = data.length;
  averageContainer.style.display = "";
  average.innerHTML = "$" + calculateAverage(data).toFixed(2);
  detailsToggle.style.display = "";
  window.filteredVehiclesData = data;
}

const timeFrameButtons = document.querySelectorAll(`[data-time-frame]`);
const originalButtonsClass = "inline-flex justify-center items-center space-x-2 border font-semibold rounded-l-lg px-4 py-2 leading-6 border-gray-200 bg-white text-gray-800 hover:z-1 hover:border-gray-300 hover:text-gray-900 hover:shadow-sm focus:z-1 focus:ring focus:ring-gray-300 focus:ring-opacity-25 active:z-1 active:border-gray-200 active:shadow-none dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:border-gray-600 dark:hover:text-gray-200 dark:focus:ring-gray-600 dark:focus:ring-opacity-40 dark:active:border-gray-700";
const activeButtonsClass = "inline-flex justify-center items-center space-x-2 border font-semibold rounded-l-lg px-4 py-2 leading-6 border-blue-700 bg-blue-700 text-white hover:z-1 hover:text-white hover:bg-blue-600 hover:border-blue-600 focus:z-1 focus:ring focus:ring-blue-400 focus:ring-opacity-50 active:z-1 active:bg-blue-700 active:border-blue-700 dark:focus:ring-blue-400 dark:focus:ring-opacity-90";
timeFrameButtons.forEach(function (btn) {
  btn.addEventListener("click", function (e) {
    // Reset Button Colors
    timeFrameButtons.forEach((each) => each.className = originalButtonsClass);

    btn.className = activeButtonsClass;
    const value = parseInt(btn.getAttribute('data-time-frame'));
    const time = form.querySelector('#sale__sale_date__gte');
    time.value = value;

    // Dispatch the event on the form element
    form.dispatchEvent(new Event("submit", {
      bubbles: true, // Allow the event to bubble up the DOM tree
      cancelable: true // Allow the event to be canceled
    }));
  });
});
