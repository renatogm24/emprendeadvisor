const optionsMenu = document.querySelectorAll(".menuProfileOpt");

function resetBtns() {
  optionsMenu.forEach((element) => {
    element.classList.remove("bg-primary", "text-light");
    element.classList.add("bg-graytheme");
  });
}

for (const option of optionsMenu) {
  option.addEventListener("click", async (e) => {
    resetBtns();
    option.classList.remove("bg-graytheme");
    option.classList.add("bg-primary", "text-light");
    optionTxt = e.target.innerText;

    if (
      [
        "Mi Perfil",
        "Mi Contraseña",
        "Mis Favoritos",
        "Usuarios",
        "Solicitud Categorias",
      ].includes(optionTxt)
    ) {
      const menu = document.querySelector(".profileMenu");
      menu.classList.add("d-none", "d-lg-block");
      const info = document.querySelector(".profileInfo");
      info.classList.remove("d-none");
      info.classList.add("d-block");

      profileForm = info.querySelector(".profileForm");

      if (optionTxt === "Mi Perfil") {
        const response = await fetch(
          "https://www.emprendeadvisor.com/getUserSession"
        );
        const data = await response.json();

        profileForm.innerHTML = "";

        const form = document.createElement("form");

        const first_name_label = document.createElement("label");
        first_name_label.classList.add("form-label", "mb-2");
        first_name_label.innerText = "Nombre:";
        form.appendChild(first_name_label);

        const first_name = document.createElement("input");
        first_name.value = data.first_name;
        first_name.name = "first_name";
        first_name.classList.add("form-control", "mb-2");
        form.appendChild(first_name);

        const last_name_label = document.createElement("label");
        last_name_label.classList.add("form-label", "mb-2");
        last_name_label.innerText = "Apellidos:";
        form.appendChild(last_name_label);

        const last_name = document.createElement("input");
        last_name.value = data.last_name;
        last_name.name = "last_name";
        last_name.classList.add("form-control", "mb-2");
        form.appendChild(last_name);

        const email_label = document.createElement("label");
        email_label.classList.add("form-label", "mb-2");
        email_label.innerText = "Correo:";
        form.appendChild(email_label);

        const email = document.createElement("input");
        email.value = data.email;
        email.name = "email";
        email.classList.add("form-control", "mb-2");
        form.appendChild(email);

        const button = document.createElement("input");
        button.classList.add("btn", "btn-altprimary", "text-light", "my-3");
        button.setAttribute("type", "submit");
        button.value = "Actualizar";
        form.appendChild(button);

        form.addEventListener("submit", (e) => {
          updateProfile(e);
        });

        profileForm.appendChild(form);
      }

      if (optionTxt === "Mi Contraseña") {
        profileForm.innerHTML = "";
        const form = document.createElement("form");

        const password_actual_label = document.createElement("label");
        password_actual_label.classList.add("form-label", "mb-2");
        password_actual_label.innerText = "Contraseña actual:";
        form.appendChild(password_actual_label);

        const password_actual = document.createElement("input");
        password_actual.value = "";
        password_actual.name = "actual_password";
        password_actual.setAttribute("type", "password");
        password_actual.classList.add("form-control", "mb-2");
        form.appendChild(password_actual);

        const password_label = document.createElement("label");
        password_label.classList.add("form-label", "mb-2");
        password_label.innerText = "Contraseña nueva:";
        form.appendChild(password_label);

        const password = document.createElement("input");
        password.value = "";
        password.name = "password";
        password.setAttribute("type", "password");
        password.classList.add("form-control", "mb-2");
        form.appendChild(password);

        const password_repeat_label = document.createElement("label");
        password_repeat_label.classList.add("form-label", "mb-2");
        password_repeat_label.innerText = "Repetir contraseña nueva:";
        form.appendChild(password_repeat_label);

        const password_repeat = document.createElement("input");
        password_repeat.value = "";
        password_repeat.name = "repeat_password";
        password_repeat.setAttribute("type", "password");
        password_repeat.classList.add("form-control", "mb-2");
        form.appendChild(password_repeat);

        const button = document.createElement("input");
        button.classList.add("btn", "btn-altprimary", "text-light", "my-3");
        button.setAttribute("type", "submit");
        button.value = "Actualizar";
        form.appendChild(button);

        form.addEventListener("submit", (e) => {
          updatePassword(e);
        });

        profileForm.appendChild(form);
      }
    }
    if (optionTxt === "Mis Favoritos") {
      profileForm.innerHTML = "";

      for (let index = 0; index < 6; index++) {
        const divContainer = document.createElement("div");
        divContainer.classList.add("col-6", "col-lg-3", "my-2");

        const divGrayBg = document.createElement("div");
        divGrayBg.classList.add("bg-graytheme", "p-2");

        const imgEmprendimiento = document.createElement("img");
        imgEmprendimiento.src = "/static/images/product.jpg";
        imgEmprendimiento.classList.add("img-fluid");

        const nameAndHeart = document.createElement("div");
        nameAndHeart.classList.add(
          "mt-3",
          "d-flex",
          "justify-content-between",
          "align-items-center"
        );

        const name = document.createElement("span");
        name.classList.add("h6");
        name.innerText = "Rumbero";

        const heart = document.createElement("span");
        heart.classList.add("h6");
        heart.innerHTML = '<i class="bi bi-heart starIcon"></i>';

        nameAndHeart.appendChild(name);
        nameAndHeart.appendChild(heart);

        const descrip = document.createElement("p");
        descrip.classList.add("my-0", "textCardEmpre");
        descrip.innerHTML =
          "¡Para todos los rumberos que lleven la salsa en la piel! Ropa salsera del Perú Hecho en algodón peruano Envíos gratis a todo el Perú";

        const stars = document.createElement("div");
        stars.classList.add("my-1", "text-yellowstar");
        stars.innerHTML =
          '<i class="bi bi-star-fill mx-1"></i><i class="bi bi-star-fill mx-1"></i><i class="bi bi-star-fill mx-1"></i><i class="bi bi-star-fill mx-1"></i><i class="bi bi-star-fill mx-1"></i>';

        const reviewCount = document.createElement("div");
        reviewCount.classList.add("mt-3", "textCardEmpre");
        reviewCount.innerHTML = "(45 calificaciones)";

        divGrayBg.appendChild(imgEmprendimiento);
        divGrayBg.appendChild(nameAndHeart);
        divGrayBg.appendChild(descrip);
        divGrayBg.appendChild(stars);
        divGrayBg.appendChild(reviewCount);

        divContainer.appendChild(divGrayBg);

        profileForm.appendChild(divContainer);
      }
    }
    if (optionTxt === "Usuarios") {
      const search = document.createElement("div");
      search.classList.add("input-group", "mb-3", "searchBx");
      search.innerHTML = `<input type="text" class="form-control inputSearch" placeholder="Buscar usuario..." aria-label="Buscar usuario" aria-describedby="basic-addon2">
  <div class="input-group-append">
    <button class="btn btn-outline-secondary searchBtn" type="button">Buscar</button>
  </div>`;

      const headers = [
        { title: "id", name: "id" },
        { title: "Nombres", name: "first_name" },
        { title: "Apellidos", name: "last_name" },
        { title: "Email", name: "email" },
        {
          title: "Actions",
          listActions: [
            {
              class: ["btn", "btn-success", "mx-lg-2"],
              type: "update users",
              getPath: (id) => {
                return `/admin/users/${id}`;
              },
              logo: "bi-pencil",
            },
            {
              class: ["btn", "btn-danger", "mx-lg-2"],
              type: "delete users",
              getPath: (id) => {
                return `/admin/users/delete/${id}`;
              },
              logo: "bi-trash",
            },
          ],
        },
      ];

      const limit = 5;

      const path = "/admin/users";

      const button = document.createElement("input");
      button.classList.add(
        "btn",
        "btn-altprimary",
        "text-light",
        "my-3",
        "LoadMoreBtn"
      );
      button.setAttribute("type", "button");
      button.value = "Cargar más registros";
      button.addEventListener("click", () => {
        tableCreate("append", profileForm, headers, path, limit);
      });

      profileForm.appendChild(button);
      profileForm.insertBefore(search, profileForm.firstChild);

      await tableCreate("create", profileForm, headers, path, limit);

      //const searchBtn = document.querySelector(".searchBtn");
      const searchBtn = document.querySelector(".inputSearch");
      searchBtn.focus();

      searchBtn.addEventListener("input", () => {
        const searchWord = document.querySelector(".inputSearch").value;
        if (searchWord === "") {
          option.click();
          return;
        }
        const path = `/admin/searchUsers/${searchWord}`;
        tableCreate("search", profileForm, headers, path, limit);
      });

      const title = document.createElement("h3");
      title.classList.add("my-2", "text-center");
      title.innerHTML = "Lista de usuarios";
      profileForm.insertBefore(title, profileForm.firstChild);
    }

    if (optionTxt === "Solicitud Categorias") {
      const search = document.createElement("div");
      search.classList.add("input-group", "mb-3");
      search.innerHTML = `<input type="text" class="form-control inputSearch" placeholder="Buscar solicitud..." aria-label="Buscar usuario" aria-describedby="basic-addon2">
  <div class="input-group-append">
    <button class="btn btn-outline-secondary searchBtn" type="button">Buscar</button>
  </div>`;

      const headers = [
        { title: "id", name: "id" },
        { title: "Emprendimiento @ig", name: "ig_url" },
        { title: "Categoría", name: "category_name" },
        { title: "Subcategoría", name: "subcategory_name" },
        {
          title: "Actions",
          listActions: [
            {
              class: ["btn", "btn-success", "mx-lg-2"],
              type: "accept categories",
              getPath: (id) => {
                return `/admin/categories/accept/${id}`;
              },
              logo: "bi-check2",
            },
            {
              class: ["btn", "btn-danger", "mx-lg-2"],
              type: "delete categories",
              getPath: (id) => {
                return `/admin/categories/delete/${id}`;
              },
              logo: "bi-x-circle",
            },
          ],
        },
      ];

      const limit = 5;

      const path = "/admin/users";

      await tableCreate("create", profileForm, headers, path, limit);

      //const searchBtn = document.querySelector(".searchBtn");
      const searchBtn = document.querySelector(".inputSearch");
      searchBtn.focus();

      searchBtn.addEventListener("input", () => {
        const searchWord = document.querySelector(".inputSearch").value;
        if (searchWord === "") {
          option.click();
          return;
        }
        const path = `/admin/searchUsers/${searchWord}`;
        tableCreate("search", profileForm, headers, path, limit);
      });

      const title = document.createElement("h3");
      title.classList.add("my-2", "text-center");
      title.innerHTML = "Lista de solicitudes";
      profileForm.insertBefore(title, profileForm.firstChild);
    }

    if (optionTxt === "Cerrar Sesión") {
      window.location.href = "/logout";
    }
  });
}

async function tableCreate(action, element, headers, path, limit) {
  let users = [];
  if (action === "create") {
    profileForm.innerHTML = "";

    const button = document.createElement("input");
    button.classList.add("btn", "btn-success", "text-light", "my-3", "col-3");
    button.setAttribute("type", "button");
    button.value = "Añadir";

    arrPath = path.split("/");
    button.addEventListener("click", (e) => {
      actionElement(
        e,
        "create " + arrPath[arrPath.length - 1],
        path + "/create"
      );
    });

    //const tableDiv = document.querySelector(".table-responsive");

    //tableDiv.parentElement.insertBefore(button, tableDiv);
    profileForm.appendChild(button);

    const buttonLoad = document.createElement("input");
    buttonLoad.classList.add(
      "btn",
      "btn-altprimary",
      "text-light",
      "my-3",
      "LoadMoreBtn"
    );
    buttonLoad.setAttribute("type", "button");
    buttonLoad.value = "Cargar más registros";
    buttonLoad.addEventListener("click", () => {
      tableCreate("append", profileForm, headers, path, limit);
    });

    //profileForm.insertBefore(buttonLoad, profileForm.firstChild);
    profileForm.appendChild(buttonLoad);

    const offset = 0;
    const link = `https://www.emprendeadvisor.com${path}/${limit}/${offset}`;
    console.log(link);

    const response = await fetch(link);
    console.log(response);
    const data = await response.json();

    if ("users" in data) {
      users = data.users;
    }

    if ("endList" in data) {
      if (data.endList) {
        const btn = document.querySelector(".LoadMoreBtn");
        btn.disabled = true;
      }
    }

    const tableBx = document.createElement("div");
    tableBx.classList.add("table-responsive");

    const tbl = document.createElement("table");
    tbl.classList.add("my-2", "table", "align-middle");

    const thead = document.createElement("thead");
    const trow = document.createElement("tr");

    for (let index = 0; index < headers.length; index++) {
      const element = headers[index];
      if (element.title !== "id") {
        const theading = document.createElement("th");
        theading.innerText = element.title;
        trow.appendChild(theading);
      }
    }

    thead.appendChild(trow);

    tbl.appendChild(thead);

    const tbody = document.createElement("tbody");

    tbl.appendChild(tbody);

    tableBx.appendChild(tbl);

    element.appendChild(tableBx);
  }

  if (action === "append") {
    let offset = document.querySelectorAll("tr").length - 1;
    if (offset < 0) {
      offset = 0;
    }
    const response = await fetch(
      `https://www.emprendeadvisor.com${path}/${limit}/${offset}`
    );
    const data = await response.json();
    if ("users" in data) {
      users = data.users;
    }

    if ("endList" in data) {
      if (data.endList) {
        const btn = document.querySelector(".LoadMoreBtn");
        btn.disabled = true;
      }
    }
  }

  if (action === "search") {
    const offset = 0;
    const response = await fetch(
      `https://www.emprendeadvisor.com${path}/${limit}/${offset}`
    );
    const data = await response.json();
    if ("users" in data) {
      users = data.users;
    }

    const btnLoadMore = document.querySelector(".LoadMoreBtn");

    const button = document.createElement("input");
    button.classList.add(
      "btn",
      "btn-altprimary",
      "text-light",
      "my-3",
      "LoadMoreBtn"
    );
    button.setAttribute("type", "button");
    button.value = "Cargar más registros";

    button.addEventListener("click", () => {
      tableCreate("append", profileForm, headers, path, limit);
    });

    element.insertBefore(button, btnLoadMore);

    btnLoadMore.remove();

    if ("endList" in data) {
      const btn = document.querySelector(".LoadMoreBtn");
      if (data.endList) {
        btn.disabled = true;
      } else {
        btn.disabled = false;
      }
    }

    const tbody = document.querySelector("tbody");
    tbody.innerHTML = "";
  }

  const tbody = document.querySelector("tbody");
  for (const user of users) {
    const trow2 = document.createElement("tr");
    for (let index = 0; index < headers.length; index++) {
      const element = headers[index];
      if (element.title !== "id") {
        if (element.title === "Actions") {
          const tdata4 = document.createElement("td");
          listActions = element.listActions;
          for (let index = 0; index < listActions.length; index++) {
            const element = listActions[index];
            const action = document.createElement("a");
            action.classList.add(...element.class);
            const logo = document.createElement("i");
            logo.classList.add("bi", element.logo, "starIcon");
            action.appendChild(logo);
            action.addEventListener("click", (e) => {
              actionElement(e, element.type, element.getPath(user.id));
            });
            tdata4.appendChild(action);
          }
          trow2.appendChild(tdata4);
        } else {
          const tdata = document.createElement("td");
          tdata.innerText = user[element.name];
          trow2.appendChild(tdata);
        }
      }
    }

    tbody.appendChild(trow2);
  }
}

async function actionElement(e, type, url) {
  const [action, dataType] = type.split(" ");
  let fields = [];

  if (dataType === "users") {
    fields = [
      { title: "id", name: "id" },
      { title: "Nombres", name: "first_name" },
      { title: "Apellidos", name: "last_name" },
      { title: "Email", name: "email" },
      { title: "Password", name: "password" },
    ];
  }

  if (action === "update" || action === "create") {
    profileForm = document.querySelector(".profileForm");
    profileForm.innerHTML = "";

    const backButton = document.createElement("button");
    backButton.classList.add(
      "btn",
      "btn-altprimary",
      "text-light",
      "my-3",
      "w-25"
    );
    const icon = document.createElement("i");
    icon.classList.add("bi", "bi-arrow-left", "starIcon", "mx-2");
    const text = document.createTextNode("Volver");
    backButton.appendChild(icon);
    backButton.appendChild(text);

    if (dataType === "users") {
      backButton.addEventListener("click", () => {
        document.querySelectorAll(".menuProfileOpt")[0].click();
        const errorLogin = document.querySelector(".errorLogin");
        errorLogin.innerText = "";
        errorLogin.classList.remove("py-3");
      });
    }

    profileForm.appendChild(backButton);

    let response = "";
    let data = {};

    if (action === "update") {
      response = await fetch(`https://www.emprendeadvisor.com${url}`);
      data = await response.json();
    }
    let result = "";
    if (dataType in data) {
      result = data[dataType];
    }
    const form = document.createElement("form");

    for (const field of fields) {
      if (field.name !== "id") {
        const field_label = document.createElement("label");
        field_label.classList.add("form-label", "mb-2");
        field_label.innerText = field.title;
        form.appendChild(field_label);
      }

      const field_input = document.createElement("input");
      if (action === "update") {
        field_input.value = result[field.name];
      } else if (action === "update") {
        field_input.value = "";
      }
      field_input.name = field.name;
      field_input.classList.add("form-control", "mb-2");
      if (field.name === "password") {
        field_input.setAttribute("type", "password");
      }
      if (field.name === "id") {
        field_input.setAttribute("type", "hidden");
      }
      form.appendChild(field_input);
    }

    const button = document.createElement("input");
    button.classList.add("btn", "btn-altprimary", "text-light", "my-3");
    button.setAttribute("type", "submit");
    if (action === "update") {
      button.value = "Actualizar";
    } else if (action === "create") {
      button.value = "Guardar";
    }

    form.appendChild(button);

    const urlArr = url.split("/");
    let newUrl = "";
    for (let index = 0; index < urlArr.length - 1; index++) {
      const element = urlArr[index];
      newUrl += element + "/";
    }
    newUrl += action;

    form.addEventListener("submit", (e) => {
      updateForm(e, newUrl);
    });

    profileForm.appendChild(form);
  }

  if (action === "delete") {
    const response = await fetch(`https://www.emprendeadvisor.com${url}`);
    const data = await response.json();
    let result = "";
    if (dataType in data) {
      result = data[dataType];
    }

    if (result < 1) {
      return;
    }

    if (e.target.tagName === "I") {
      e.target.parentElement.parentElement.parentElement.remove();
    } else if (e.target.tagName === "A") {
      e.target.parentElement.parentElement.remove();
    } else if (e.target.tagName === "TD") {
      e.target.parentElement.remove();
    }
  }
}

async function updateForm(event, url) {
  event.preventDefault();
  const errorLogin = document.querySelector(".errorLogin");
  const success = document.querySelector(".success");

  errorLogin.innerText = "";
  errorLogin.classList.remove("py-3");

  success.innerText = "";

  const form = new FormData(event.target);
  const response = await fetch(`https://www.emprendeadvisor.com${url}`, {
    method: "POST",
    body: form,
  });
  const data = await response.json();
  if ("error" in data) {
    errorLogin.innerText = data.error;
    errorLogin.classList.add("py-3");
  } else if (data.updated) {
    success.innerText = "Se ha sido actualizado correctamente";
    success.classList.add("py-3");
    setTimeout(() => {
      success.innerText = "";
      success.classList.remove("py-3");
    }, 3000);
  } else if (data.created) {
    success.innerText = "Se ha creado el nuevo registro";
    success.classList.add("py-3");
    setTimeout(() => {
      success.innerText = "";
      success.classList.remove("py-3");
    }, 3000);
  }
}

async function updateProfile(event) {
  event.preventDefault();
  const errorLogin = document.querySelector(".errorLogin");
  const success = document.querySelector(".success");

  errorLogin.innerText = "";
  errorLogin.classList.remove("py-3");

  success.innerText = "";

  const form = new FormData(event.target);
  const response = await fetch(
    "https://www.emprendeadvisor.com/updateProfile",
    {
      method: "POST",
      body: form,
    }
  );
  const data = await response.json();
  if ("error" in data) {
    errorLogin.innerText = data.error;
    errorLogin.classList.add("py-3");
  } else if (data.updated) {
    success.innerText = "El usuario ha sido actualizado correctamente";
    success.classList.add("py-3");
    const helloBx = document.querySelector(".helloBx");
    helloBx.innerText = `¡Hola ${form.get("first_name")} ${form.get(
      "last_name"
    )}!`;
    setTimeout(() => {
      success.innerText = "";
      success.classList.remove("py-3");
    }, 3000);
  }
}

async function updatePassword(event) {
  event.preventDefault();
  const errorLogin = document.querySelector(".errorLogin");
  const success = document.querySelector(".success");

  errorLogin.innerText = "";
  errorLogin.classList.remove("py-3");

  success.innerText = "";

  const form = new FormData(event.target);

  if (
    form.get("repeat_password") !== form.get("password") ||
    form.get("password").length < 6
  ) {
    errorLogin.innerText =
      "Las contraseñas no coinciden o contiene menos de 6 caracteres";
    errorLogin.classList.add("py-3");
    return;
  }

  const response = await fetch(
    "https://www.emprendeadvisor.com/updatePassword",
    {
      method: "POST",
      body: form,
    }
  );
  const data = await response.json();
  if ("error" in data) {
    errorLogin.innerText = data.error;
    errorLogin.classList.add("py-3");
  } else if (data.updated) {
    success.innerText = "La contraseña ha sido actualizada correctamente";
    success.classList.add("py-3");
    setTimeout(() => {
      success.innerText = "";
      success.classList.remove("py-3");
    }, 3000);
  }
}

function backMenu() {
  resetBtns();
  const menu = document.querySelector(".profileMenu");
  menu.classList.remove("d-none", "d-lg-block");
  const info = document.querySelector(".profileInfo");
  info.classList.remove("d-block");
  info.classList.add("d-none");
  profileForm = info.querySelector(".profileForm");
  profileForm.innerHTML = "";
}
