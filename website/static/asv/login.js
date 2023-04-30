const form = document.getElementById("login-form");
const errorNotice = document.getElementById("login-error");

form.addEventListener("submit", function (e) {
    e.preventDefault();
  
    const values = Object.fromEntries(new FormData(e.target));
  
    fetch("/login", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(values),
      credentials: "include",
    })
      .catch(({ data }) => {
        errorNotice.style.display = "";
        console.error(data);
      });
  });