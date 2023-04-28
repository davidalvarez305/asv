const form = document.getElementById("filter-trucks-form");
const counter = document.getElementById("data-counter");
const counterContainer = document.getElementById("data-counter-container");
const average = document.getElementById("data-average");
const averageContainer = document.getElementById("data-average-container");

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
    })
    .catch(console.error);
});

function calculateAverage(data) {
  return data.reduce((total, current) => total + parseFloat(current.saleprice), 0) / data.length;
}
