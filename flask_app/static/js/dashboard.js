const emprendimientosBx = document.querySelector("#emprendimientosBx");

const loadMoreEmp = document.querySelector("#loadMoreEmp");

loadMoreEmp.addEventListener("submit", async (e) => {
  e.preventDefault();

  offset = emprendimientosBx.querySelectorAll(".empreBox").length;

  const form = new FormData(loadMoreEmp);
  form.append("offset", offset);

  const pathCategory = document.querySelector("#pathCategory");

  if (pathCategory.value != "0") {
    form.append("category_id", pathCategory.value);
  }

  const response = await fetch(
    "https://www.emprendeadvisor.com/emprendimientos/loadmore",
    {
      method: "POST",
      body: form,
    }
  );

  const data = await response.json();

  for (emprendimiento of data.emprendimientos) {
    emprendimientosBx.appendChild(createEmprendimiento(emprendimiento));
  }

  if ("endList" in data) {
    if (data.endList) {
      const btn = document.querySelector(".btnLoadMoreEmp");
      btn.disabled = true;
    }
  }
});

const empOrderSelector = document.querySelector("#empOrderSelector");
empOrderSelector.addEventListener("change", async (e) => {
  const btn = document.querySelector(".btnLoadMoreEmp");
  emprendimientosBx.innerHTML = "";
  const selectorOrder = document.querySelector("#order_by");

  selectorOrder.value = e.target.value;

  offset = emprendimientosBx.querySelectorAll(".empreBox").length;

  const form = new FormData(loadMoreEmp);
  form.append("offset", offset);

  const pathCategory = document.querySelector("#pathCategory");

  if (pathCategory.value != "0") {
    form.append("category_id", pathCategory.value);
  }

  const response = await fetch(
    "https://www.emprendeadvisor.com/emprendimientos/loadmore",
    {
      method: "POST",
      body: form,
    }
  );

  const data = await response.json();

  for (emprendimiento of data.emprendimientos) {
    emprendimientosBx.appendChild(createEmprendimiento(emprendimiento));
  }

  if ("endList" in data) {
    if (data.endList) {
      btn.disabled = true;
    }
  }

  btn.disabled = false;
});

const filter1 = document.querySelector("#filter1");
const filter2 = document.querySelector("#filter2");

filter1.addEventListener("click", async () => {
  const btn = document.querySelector(".btnLoadMoreEmp");

  const min_promedio = document.querySelector("#min_promedio");
  const max_promedio = document.querySelector("#max_promedio");
  const min_reviews = document.querySelector("#min_reviews");
  const max_reviews = document.querySelector("#max_reviews");
  const min_followers = document.querySelector("#min_followers");
  const max_followers = document.querySelector("#max_followers");

  min_promedio.value = document.querySelector("#range1").innerHTML;
  max_promedio.value = document.querySelector("#range2").innerHTML;
  min_reviews.value = document.querySelector("#range3").innerHTML;
  max_reviews.value = document.querySelector("#range4").innerHTML;
  min_followers.value = document.querySelector("#range5").innerHTML;
  max_followers.value = document.querySelector("#range6").innerHTML;

  emprendimientosBx.innerHTML = "";

  offset = emprendimientosBx.querySelectorAll(".empreBox").length;

  const form = new FormData(loadMoreEmp);
  form.append("offset", offset);

  const pathCategory = document.querySelector("#pathCategory");

  if (pathCategory.value != "0") {
    form.append("category_id", pathCategory.value);
  }

  const response = await fetch(
    "https://www.emprendeadvisor.com/emprendimientos/loadmore",
    {
      method: "POST",
      body: form,
    }
  );

  const data = await response.json();

  for (emprendimiento of data.emprendimientos) {
    emprendimientosBx.appendChild(createEmprendimiento(emprendimiento));
  }

  if ("endList" in data) {
    if (data.endList) {
      btn.disabled = true;
    }
  }

  btn.disabled = false;
});

filter2.addEventListener("click", async () => {
  const btn = document.querySelector(".btnLoadMoreEmp");

  const min_promedio = document.querySelector("#min_promedio");
  const max_promedio = document.querySelector("#max_promedio");
  const min_reviews = document.querySelector("#min_reviews");
  const max_reviews = document.querySelector("#max_reviews");
  const min_followers = document.querySelector("#min_followers");
  const max_followers = document.querySelector("#max_followers");

  min_promedio.value = document.querySelector("#range7").innerHTML;
  max_promedio.value = document.querySelector("#range8").innerHTML;
  min_reviews.value = document.querySelector("#range9").innerHTML;
  max_reviews.value = document.querySelector("#range10").innerHTML;
  min_followers.value = document.querySelector("#range11").innerHTML;
  max_followers.value = document.querySelector("#range12").innerHTML;

  emprendimientosBx.innerHTML = "";

  offset = emprendimientosBx.querySelectorAll(".empreBox").length;

  const form = new FormData(loadMoreEmp);
  form.append("offset", offset);

  const pathCategory = document.querySelector("#pathCategory");

  if (pathCategory.value != "0") {
    form.append("category_id", pathCategory.value);
  }

  const response = await fetch(
    "https://www.emprendeadvisor.com/emprendimientos/loadmore",
    {
      method: "POST",
      body: form,
    }
  );

  const data = await response.json();

  for (emprendimiento of data.emprendimientos) {
    emprendimientosBx.appendChild(createEmprendimiento(emprendimiento));
  }

  if ("endList" in data) {
    if (data.endList) {
      btn.disabled = true;
    }
  }

  btn.disabled = false;

  const closeOffCanvas = document.querySelector("#closeOffCanvas");
  closeOffCanvas.click();
});

function createEmprendimiento(emprendimiento) {
  const newCard = document.createElement("div");
  newCard.classList.add("col-6", "col-lg-3", "my-2", "empreBox");
  const stars = Math.round(emprendimiento.promedio);
  const remain = 5 - stars;

  let text = "";

  for (let index = 0; index < stars; index++) {
    text += `<i class="bi bi-star-fill mx-1"></i>`;
  }

  for (let index = 0; index < remain; index++) {
    text += `<i class="bi bi-star mx-1"></i>`;
  }

  let calificacion = "";
  if (emprendimiento.cuenta == 0) {
    calificacion = "Sin calificar";
  } else if (emprendimiento.cuenta == 1) {
    calificacion = "(1 calificación)";
  } else {
    calificacion = `(${emprendimiento.cuenta} calificaciones)`;
  }

  newCard.innerHTML = `<div class="bg-graytheme p-2">
                    <a
                    href="/emprendimiento/${emprendimiento.id}"
                    style="cursor: pointer"
                    >                
                    <img
                    class="img-fluid"
                    src="https://www.emprendeadvisor.com/img/${emprendimiento.url_p1}&${emprendimiento.url_p2}"
                    alt=""
                  /></a>
                  <div
                    class="mt-3 d-flex justify-content-between align-items-center"
                  >
                    <span
                      class="h6"
                      style="line-height: 1.5em; height: 3em; overflow: hidden"
                      >${emprendimiento.full_name}</span
                    >                    
                  </div>
                  <p class="my-0 textCardEmpre">${emprendimiento.biography}</p>
                  <div class="my-1 text-yellowstar">
                    ${text}
                  </div>
                  <div class="mt-3 textCardEmpre">
                    ${calificacion}
                  </div>
                </div>`;
  return newCard;
}
