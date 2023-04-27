const form = document.getElementById("filter-trucks-form");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  var formData = Object.fromEntries(new FormData(e.target).entries());

  fetch(e.method, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    credentials: "include",
    body: JSON.stringify(formData),
  })
    .then((response) => response.json())
    .then(console.log)
    .catch(console.error);
});
