window.onload = function () {
  const allInputs = document.querySelectorAll(".star-widget input");
  for (input of allInputs) {
    input.addEventListener("click", (e) => {
      console.log(e.target.id.split("-")[1]);
    });
  }
};

const loginForm = document.querySelector("#loginForm");
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(loginForm);
  form.append("pathname", window.location.pathname);
  const response = await fetch("https://www.emprendeadvisor.com/login", {
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
  form.append("pathname", window.location.pathname);
  const response = await fetch(
    "https://www.emprendeadvisor.com/register/user",
    {
      method: "POST",
      body: form,
      credentials: "same-origin",
    }
  );
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

document.addEventListener("click", function (e) {
  // Hamburger menu
  if (e.target.classList.contains("hamburger-toggle")) {
    e.target.children[0].classList.toggle("active");
  }
});

/* -------*/

function checkNewCategory(element) {
  inputCategory1 = document.querySelector("#categoria");
  inputCategory2 = document.querySelector("#subcategoria");
  newInput1 = document.querySelectorAll(".newInput")[0];
  if (element.checked) {
    inputCategory1.disabled = true;
    inputCategory2.disabled = true;
    newInput1.classList.toggle("active");
  } else {
    inputCategory1.disabled = false;
    inputCategory2.disabled = false;
    newInput1.classList.toggle("active");
  }
}

function checkNewSubcategory(element) {
  newInput2 = document.querySelectorAll(".newInput")[1];
  if (element.checked) {
    newInput2.classList.toggle("active");
  } else {
    newInput2.classList.toggle("active");
  }
}

const clasificarForm = document.querySelector(".clasificarForm");

const searchForm = document.querySelector("#searchForm");
searchForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  window.location.href = "/search/" + formData.get("search");
});
