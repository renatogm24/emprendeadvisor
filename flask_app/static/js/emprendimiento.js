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

const clasificarForm = document.querySelector("#clasificarForm");

const selectFormClasif = document.querySelector("#categoria");
const selectFormSubcat = document.querySelector("#subcategoria");

try {
  selectFormClasif.addEventListener("change", async (e) => {
    const categorySelected = e.target.value;
    const response = await fetch(
      "https://www.emprendeadvisor.com/subcategories/" + categorySelected
    );
    const data = await response.json();
    selectFormSubcat.innerHTML = "";
    newOpt = document.createElement("option");
    newOpt.value = 0;
    newOpt.innerHTML = "-- Seleccion subcategoría --";
    selectFormSubcat.appendChild(newOpt);
    for (category of data.categories) {
      newOpt = document.createElement("option");
      newOpt.value = category.id;
      newOpt.innerHTML = category.name;
      selectFormSubcat.appendChild(newOpt);
    }
  });
} catch (error) {
  console.log("Error");
}

try {
  clasificarForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    success = document.querySelector(".successCategory");
    success.innerHTML = "";
    success.classList.remove("p-3");
    error = document.querySelector(".errorCategory");
    error.innerHTML = "";
    error.classList.remove("p-3");
    const formData = new FormData(e.target);

    checkCat = document.querySelector("#categoriaCheckBx").checked;
    checkSub = document.querySelector("#subcategoriaCheckBx").checked;
    selectCat = document.querySelector("#categoria").value;
    selectSub = document.querySelector("#subcategoria").value;

    if (!checkCat) {
      if (selectCat === "0" || selectCat === "0") {
        error.innerHTML = "Debes ingresar una categoría y subcategoría valida";
        error.classList.add("p-3");
        return;
      }
    }

    if (checkCat && !checkSub) {
      if (formData.get("nuevaCategoria").length < 1) {
        error.innerHTML = "El nombre de la categoría no puede estar vacío";
        error.classList.add("p-3");
        return;
      }
    }

    if (checkCat && checkSub) {
      if (
        formData.get("nuevaCategoria").length < 1 ||
        formData.get("nuevaSubcategoria").length < 1
      ) {
        error.innerHTML = "Los nombres de categorías no pueden estar vacíos";
        error.classList.add("p-3");
        return;
      }
    }

    formData.append("pathname", window.location.pathname);
    const response = await fetch(
      "https://www.emprendeadvisor.com/categories/create",
      {
        method: "POST",
        body: formData,
      }
    );
    const data = await response.json();
    if ("error" in data) {
      error.innerHTML = "Ya existe la categoría";
      error.classList.add("p-3");
      return;
    }
    if ("created" in data) {
      success.innerHTML = "La solicitud de categoria ha sido enviada";
      success.classList.add("p-3");
      setTimeout(() => {
        const modalCloseBtn = document.querySelector(".closeModalClas");
        modalCloseBtn.click();
      }, 1500);
    }
    if ("redirect" in data) {
      if (data.redirect === true) {
        window.location.href = data.url;
      }
    }
  });
} catch (error) {
  console.log("Error");
}

const searchForm = document.querySelector("#searchForm");
searchForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  window.location.href = "/search/" + formData.get("search");
});
