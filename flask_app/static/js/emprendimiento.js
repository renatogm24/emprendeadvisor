window.onload = function () {
  const allInputs = document.querySelectorAll(".star-widget input");
  for (input of allInputs) {
    input.addEventListener("click", (e) => {});
  }
};

const loginForm = document.querySelector("#loginForm");
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(loginForm);
  form.append("pathname", window.location.pathname);
  const response = await fetch("http://18.205.29.39:5001/login", {
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
  const response = await fetch("http://18.205.29.39:5001/register/user", {
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
      "http://18.205.29.39:5001/subcategories/" + categorySelected
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
} catch (error) {}

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
    const response = await fetch("http://18.205.29.39:5001/categories/create", {
      method: "POST",
      body: formData,
    });
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
} catch (error) {}

const searchForm = document.querySelector("#searchForm");
searchForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  window.location.href = "/search/" + formData.get("search");
});

listenerLikesButtons();

const commentsBx = document.querySelector("#commentsBx");

const loadMoreCom = document.querySelector("#loadMoreCom");

loadMoreCom.addEventListener("submit", async (e) => {
  e.preventDefault();

  offset = commentsBx.querySelectorAll(".commentBx").length;

  const form = new FormData(loadMoreCom);
  form.append("offset", offset);

  const response = await fetch(
    "http://18.205.29.39:5001/comentarios/loadmore",
    {
      method: "POST",
      body: form,
    }
  );

  const data = await response.json();

  for (review of data.reviews) {
    commentsBx.appendChild(createReview(review));
    const commentsBxArr = document.querySelectorAll(".commentBx");
    const lastBx =
      commentsBxArr[commentsBxArr.length - 1].querySelector(".likeButton");
    lastBx.addEventListener("click", async (e) => {
      const id_session_hidden =
        document.querySelector("#id_session_hidden").value;
      if (id_session_hidden != "0") {
        let id;
        let elementStart;
        if (e.target.tagName == "A") {
          id = e.target.id;
          elementStart = e.target;
        } else if (e.target.tagName == "I") {
          id = e.target.parentElement.id;
          elementStart = e.target.parentElement;
        }

        id = id.split("-")[1];

        const likeButtonIcon = elementStart.querySelector(".likeButtonIcon");

        const elementCount = elementStart.parentElement.parentElement
          .querySelectorAll(".commentBxMsg")[1]
          .querySelector(".likesCountSpan");

        if (likeButtonIcon.classList.contains("bi-hand-thumbs-up")) {
          elementCount.innerHTML = parseInt(elementCount.innerHTML) + 1;
          likeButtonIcon.classList.remove("bi-hand-thumbs-up");
          likeButtonIcon.classList.add("bi-hand-thumbs-down");
        } else {
          elementCount.innerHTML = parseInt(elementCount.innerHTML) - 1;
          likeButtonIcon.classList.remove("bi-hand-thumbs-down");
          likeButtonIcon.classList.add("bi-hand-thumbs-up");
        }

        await fetch("http://18.205.29.39:5001/like/" + id);
      } else {
        const writeOpinionBtn = document.querySelector("#writeOpinionBtn");
        writeOpinionBtn.click();
      }
    });
  }

  if ("endList" in data) {
    if (data.endList) {
      const btn = document.querySelector(".btnLoadMoreCom");
      btn.disabled = true;
    }
  }
});

function createReview(review) {
  const id_session_hidden = document.querySelector("#id_session_hidden").value;

  const newCard = document.createElement("div");
  newCard.classList.add("d-flex", "flex-column", "my-3", "commentBx");

  const stars = Math.round(review.rating);
  const remain = 5 - stars;

  let textRating = "";

  for (let index = 0; index < stars; index++) {
    textRating += `<i class="bi bi-star-fill mx-1 starIcon"></i>`;
  }

  for (let index = 0; index < remain; index++) {
    textRating += `<i class="bi bi-star mx-1 starIcon"></i>`;
  }

  let thumbsText = "";

  let thumbIcon = "";

  if (review.isLikedBySession) {
    thumbIcon = `<i class="bi bi-hand-thumbs-down starIcon likeButtonIcon"></i>`;
  } else {
    thumbIcon = `<i class="bi bi-hand-thumbs-up starIcon likeButtonIcon"></i>`;
  }

  if (id_session_hidden != review.user.id) {
    thumbsText = `<div class="d-flex align-items-center">
                  <a
                    class="btn btn-tertiary text-dark px-4 likeButton"
                    id="review-${review.id}"
                    >Útil ${thumbIcon}
                  </a>
            <a class="mx-3 border-start border-1 border-dark px-3" data-bs-toggle="modal" data-bs-target="#report" style="cursor: pointer">Informar de un abuso</a
                  >
                </div>`;
  }

  const dateFormat = new Date(review.created_at);
  const formatdate = dateFormat.toLocaleDateString();

  images = "";
  for (image of review.images) {
    images += `<img
                    src="${image.url}"
                    alt=""
                    class="imageReview mx-1"
                    onclick="img_box(this)"
                  />`;
  }

  newCard.innerHTML = `<div class="d-flex align-items-center">
                  <img
                    src=${review.user.image}
                    class=""
                    data-src=${review.user.image}
                  />
                  <span class="mx-2"
                    >${review.user.first_name} ${review.user.last_name}</span
                  >
                </div>
                <div
                  class="d-flex flex-column flex-lg-row align-items-lg-center"
                >
                  <div class="d-flex text-yellowstar my-2">
                    ${textRating}
                  </div>
                  <div class="mx-lg-2 my-2 my-lg-0 commentBxTitle">
                    ${review.title}
                  </div>
                </div>
                <div class="commentBxDate">
                  Calificado en ${review.distrito} el
                  ${formatdate}
                </div>
                <p class="commentBxMsg my-2">${review.comment}</p>
                <div class="flex">
                  ${images}
                </div>
                <div id="fullpage" onclick="this.style.display='none';"></div>
                <p class="commentBxMsg my-2">
                  A
                  <span class="likesCountSpan">${review.likesCount}</span>
                  personas les resultó útil
                </p>
                ${thumbsText}`;

  return newCard;
}

function listenerLikesButtons() {
  const likesBtns = document.querySelectorAll(".likeButton");
  for (likeBtn of likesBtns) {
    likeBtn.addEventListener("click", async (e) => {
      const id_session_hidden =
        document.querySelector("#id_session_hidden").value;
      if (id_session_hidden != "0") {
        let id;
        let elementStart;
        if (e.target.tagName == "A") {
          id = e.target.id;
          elementStart = e.target;
        } else if (e.target.tagName == "I") {
          id = e.target.parentElement.id;
          elementStart = e.target.parentElement;
        }

        id = id.split("-")[1];

        const likeButtonIcon = elementStart.querySelector(".likeButtonIcon");

        const elementCount = elementStart.parentElement.parentElement
          .querySelectorAll(".commentBxMsg")[1]
          .querySelector(".likesCountSpan");

        if (likeButtonIcon.classList.contains("bi-hand-thumbs-up")) {
          elementCount.innerHTML = parseInt(elementCount.innerHTML) + 1;
          likeButtonIcon.classList.remove("bi-hand-thumbs-up");
          likeButtonIcon.classList.add("bi-hand-thumbs-down");
        } else {
          elementCount.innerHTML = parseInt(elementCount.innerHTML) - 1;
          likeButtonIcon.classList.remove("bi-hand-thumbs-down");
          likeButtonIcon.classList.add("bi-hand-thumbs-up");
        }

        await fetch("http://18.205.29.39:5001/like/" + id);
      } else {
        const writeOpinionBtn = document.querySelector("#writeOpinionBtn");
        writeOpinionBtn.click();
      }
    });
  }
}

async function filterReview(rating) {
  const btn = document.querySelector(".btnLoadMoreCom");
  btn.disabled = false;

  commentsBx.innerHTML = "";
  offset = commentsBx.querySelectorAll(".commentBx").length;

  const ratingInput = document.querySelector("#rating_hidden");
  ratingInput.value = rating;

  const form = new FormData(loadMoreCom);
  form.append("offset", offset);

  const response = await fetch(
    "http://18.205.29.39:5001/comentarios/loadmore",
    {
      method: "POST",
      body: form,
    }
  );

  const data = await response.json();

  for (review of data.reviews) {
    commentsBx.appendChild(createReview(review));
  }

  if ("endList" in data) {
    if (data.endList) {
      const btn = document.querySelector(".btnLoadMoreCom");
      btn.disabled = true;
    }
  }

  listenerLikesButtons();
}

function setRating(rating) {
  ratingValue = document.querySelector("#rating");
  ratingValue.value = rating;
}

const reviewForm = document.querySelector("#reviewForm");
reviewForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const form = new FormData(reviewForm);

  const response = await fetch("http://18.205.29.39:5001/comentarios/crear", {
    method: "POST",
    body: form,
  });

  const data = await response.json();

  if ("error" in data) {
    const errorReview = document.querySelector(".errorReview");
    errorReview.innerText = data.error;
    errorReview.classList.add("py-3");
  } else if (data.created == true) {
    location.reload();
  }
});

const reportForm = document.querySelector("#reportForm");
reportForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const form = new FormData(reportForm);

  const response = await fetch("http://18.205.29.39:5001/comentarios/report", {
    method: "POST",
    body: form,
  });

  const data = await response.json();

  if ("error" in data) {
    const errorReview = document.querySelector(".errorReport");
    errorReview.innerText = data.error;
    errorReview.classList.add("py-3");
  } else if (data.created == true) {
    location.reload();
  }
});

function setReviewId(id) {
  const reviewForm = document.querySelector("#review_id_hidden");
  reviewForm.value = id;
}
