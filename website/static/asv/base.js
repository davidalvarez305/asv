const logout = document.getElementById("nav-logout");

logout.addEventListener("click", function () {
  const csrftoken = getCookie("csrftoken");
  fetch("/logout", {
    headers: {
      "X-CSRFToken": csrftoken,
    },
    method: "POST",
    credentials: "include",
  })
    .then((response) => response.ok && window.location.replace("/login"))
    .catch(console.error);
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
