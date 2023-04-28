const form = document.getElementById("filter-trucks-form");

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
    .then(console.log)
    .catch(console.error);
});
