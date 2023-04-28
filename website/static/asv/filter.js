const form = document.getElementById("filter-trucks-form");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  var formData = new URLSearchParams(Object.fromEntries(new FormData(e.target).entries()));

  fetch("/trucks?" + formData.toString(), {
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
