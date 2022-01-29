window.addEventListener("scroll", function () {
  const nav = document.querySelector(".homeNavbar");
  nav.classList.toggle("sticky", window.scrollY > 0);
  const span = nav.querySelector("h3");
  span.classList.toggle("text-altprimary", window.scrollY > 0);
  welcomeMsg = document.querySelector(".welcomeMsg");
  welcomeMsg.classList.toggle("text-altprimary", window.scrollY > 0);
});

const loginForm = document.querySelector("#loginForm");
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(loginForm);
  const response = await fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    body: form,
    credentials: "same-origin",
  });
  const data = await response.json();
  if ("error" in data) {
    const errorLogin = document.querySelector(".errorLogin");
    errorLogin.innerText = data.error;
    errorLogin.classList.add("py-3");
  } else if (data.isRedirect) {
    window.location.href = data.redirectUrl;
  }
});

const registerForm = document.querySelector("#registerForm");
registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorLogin = document.querySelector(".errorRegister");
  errorLogin.innerHTML = "";
  errorLogin.classList.remove("py-3");

  if (!document.querySelector("#terminosCheckBx").checked) {
    errorLogin.innerHTML += "Necesitas aceptar terminos y condiciones <br>";
    errorLogin.classList.add("py-3");
    return;
  }

  const form = new FormData(registerForm);
  const response = await fetch("http://127.0.0.1:5000/register/user", {
    method: "POST",
    body: form,
    credentials: "same-origin",
  });
  const data = await response.json();
  if ("error" in data) {
    for (error of data.error) {
      errorLogin.innerHTML += error + "<br>";
    }
    errorLogin.classList.add("py-3");
  } else if (data.isRedirect) {
    window.location.href = data.redirectUrl;
  }
});

/* MEGAMENU TOGGLER */

document.addEventListener("click", function(e) {
  // Hamburger menu
  if (e.target.classList.contains("hamburger-toggle")) {
      e.target.children[0].classList.toggle("active");
  }
});

/* -------*/