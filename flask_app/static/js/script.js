window.addEventListener("scroll", function () {
  const nav = document.querySelector(".homeNavbar");
  if (nav != null) {
    nav.classList.toggle("sticky", window.scrollY > 0);
    const span = nav.querySelector("h3");
    span.classList.toggle("text-altprimary", window.scrollY > 0);
    welcomeMsg = document.querySelector(".welcomeMsg");
    welcomeMsg.classList.toggle("text-altprimary", window.scrollY > 0);
  }
});

const loginForm = document.querySelector("#loginForm");
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(loginForm);
  form.append("pathname", window.location.pathname);
  const response = await fetch("http://127.0.0.1/login", {
    method: "POST",
    body: form,
    credentials: "include",
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

try {
  const searchForm = document.querySelector("#searchForm");
  searchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    window.location.href = "/search/" + formData.get("search");
  });
} catch (error) {
  console.log("Error");
}

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
  const response = await fetch("http://127.0.0.1/register/user", {
    method: "POST",
    body: form,
    credentials: "include",
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

/* --------SLIDER -----------*/

let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let displayValOne = document.getElementById("range1");
let displayValTwo = document.getElementById("range2");
let minGap = 0;
let sliderTrack = document.querySelector(".slider-track");
let sliderMaxValue = document.getElementById("slider-1");

function slideOne() {
  if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
    sliderOne.value = parseInt(sliderTwo.value) - minGap;
  }
  displayValOne.textContent = (sliderOne.value / 100).toFixed(1);
  fillColor();
}
function slideTwo() {
  if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
    sliderTwo.value = parseInt(sliderOne.value) + minGap;
  }
  displayValTwo.textContent = (sliderTwo.value / 100).toFixed(1);
  fillColor();
}
function fillColor() {
  percent1 = (sliderOne.value / sliderMaxValue.max) * 100;
  percent2 = (sliderTwo.value / sliderMaxValue.max) * 100;
  sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #192d4a ${percent1}% , #192d4a ${percent2}%, #dadae5 ${percent2}%)`;
}

/* ------------------------------- */

/* --------SLIDER2 -----------*/

window.onload = function () {
  const sliders = document.querySelector(".container-slider");
  if (sliders != null) {
    slideOne();
    slideTwo();
    slide3();
    slide4();
    slide5();
    slide6();
    slide7();
    slide8();
    slide9();
    slide10();
    slide11();
    slide12();
  }
};

let slider3 = document.getElementById("slider-3");
let slider4 = document.getElementById("slider-4");
let displayVal3 = document.getElementById("range3");
let displayVal4 = document.getElementById("range4");
let minGap2 = 0;
let sliderTrack2 = document.querySelectorAll(".slider-track")[1];
let sliderMaxValue2 = document.getElementById("slider-3");

function slide3() {
  if (parseInt(slider4.value) - parseInt(slider3.value) <= minGap2) {
    slider3.value = parseInt(slider4.value) - minGap2;
  }
  displayVal3.textContent = slider3.value;
  fillColor2();
}

function slide4() {
  if (parseInt(slider4.value) - parseInt(slider3.value) <= minGap2) {
    slider4.value = parseInt(slider3.value) + minGap2;
  }
  displayVal4.textContent = slider4.value;
  fillColor2();
}

function fillColor2() {
  percent1 = (slider3.value / sliderMaxValue2.max) * 100;
  percent2 = (slider4.value / sliderMaxValue2.max) * 100;
  sliderTrack2.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #192d4a ${percent1}% , #192d4a ${percent2}%, #dadae5 ${percent2}%)`;
}

/* ------------------------------- */

/* --------SLIDER3 -----------*/

let slider5 = document.getElementById("slider-5");
let slider6 = document.getElementById("slider-6");
let displayVal5 = document.getElementById("range5");
let displayVal6 = document.getElementById("range6");
let minGap3 = 0;
let sliderTrack3 = document.querySelectorAll(".slider-track")[2];
let sliderMaxValue3 = document.getElementById("slider-5");

function slide5() {
  if (parseInt(slider6.value) - parseInt(slider5.value) <= minGap3) {
    slider5.value = parseInt(slider6.value) - minGap3;
  }
  displayVal5.textContent = slider5.value;
  fillColor3();
}

function slide6() {
  if (parseInt(slider6.value) - parseInt(slider5.value) <= minGap3) {
    slider6.value = parseInt(slider5.value) + minGap3;
  }
  displayVal6.textContent = slider6.value;
  fillColor3();
}

function fillColor3() {
  percent1 = (slider5.value / sliderMaxValue3.max) * 100;
  percent2 = (slider6.value / sliderMaxValue3.max) * 100;
  sliderTrack3.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #192d4a ${percent1}% , #192d4a ${percent2}%, #dadae5 ${percent2}%)`;
}

/* ------------------------------- */

/* --------SLIDER4 -----------*/

let slider7 = document.getElementById("slider-7");
let slider8 = document.getElementById("slider-8");
let displayVal7 = document.getElementById("range7");
let displayVal8 = document.getElementById("range8");
let minGap4 = 0;
let sliderTrack4 = document.querySelectorAll(".slider-track")[3];
let sliderMaxValue4 = document.getElementById("slider-7");

function slide7() {
  if (parseInt(slider8.value) - parseInt(slider7.value) <= minGap4) {
    slider7.value = parseInt(slider7.value) - minGap4;
  }
  displayVal7.textContent = slider7.value;
  fillColor4();
}

function slide8() {
  if (parseInt(slider8.value) - parseInt(slider7.value) <= minGap4) {
    slider8.value = parseInt(slider8.value) + minGap4;
  }
  displayVal8.textContent = slider8.value;
  fillColor4();
}

function fillColor4() {
  percent1 = (slider7.value / sliderMaxValue4.max) * 100;
  percent2 = (slider8.value / sliderMaxValue4.max) * 100;
  sliderTrack4.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #192d4a ${percent1}% , #192d4a ${percent2}%, #dadae5 ${percent2}%)`;
}

/* ------------------------------- */

/* --------SLIDER5 -----------*/

let slider9 = document.getElementById("slider-9");
let slider10 = document.getElementById("slider-10");
let displayVal9 = document.getElementById("range9");
let displayVal10 = document.getElementById("range10");
let minGap5 = 0;
let sliderTrack5 = document.querySelectorAll(".slider-track")[4];
let sliderMaxValue5 = document.getElementById("slider-9");

function slide9() {
  if (parseInt(slider10.value) - parseInt(slider9.value) <= minGap5) {
    slider9.value = parseInt(slider9.value) - minGap5;
  }
  displayVal9.textContent = slider9.value;
  fillColor5();
}

function slide10() {
  if (parseInt(slider10.value) - parseInt(slider9.value) <= minGap5) {
    slider10.value = parseInt(slider10.value) + minGap5;
  }
  displayVal10.textContent = slider10.value;
  fillColor5();
}

function fillColor5() {
  percent1 = (slider9.value / sliderMaxValue5.max) * 100;
  percent2 = (slider10.value / sliderMaxValue5.max) * 100;
  sliderTrack5.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #192d4a ${percent1}% , #192d4a ${percent2}%, #dadae5 ${percent2}%)`;
}

/* ------------------------------- */

/* --------SLIDER6 -----------*/

let slider11 = document.getElementById("slider-11");
let slider12 = document.getElementById("slider-12");
let displayVal11 = document.getElementById("range11");
let displayVal12 = document.getElementById("range12");
let minGap6 = 0;
let sliderTrack6 = document.querySelectorAll(".slider-track")[5];
let sliderMaxValue6 = document.getElementById("slider-11");

function slide11() {
  if (parseInt(slider12.value) - parseInt(slider11.value) <= minGap6) {
    slider11.value = parseInt(slider11.value) - minGap6;
  }
  displayVal11.textContent = slider11.value;
  fillColor6();
}

function slide12() {
  if (parseInt(slider12.value) - parseInt(slider11.value) <= minGap6) {
    slider12.value = parseInt(slider12.value) + minGap6;
  }
  displayVal12.textContent = slider12.value;
  fillColor6();
}

function fillColor6() {
  percent1 = (slider11.value / sliderMaxValue6.max) * 100;
  percent2 = (slider12.value / sliderMaxValue6.max) * 100;
  sliderTrack6.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #192d4a ${percent1}% , #192d4a ${percent2}%, #dadae5 ${percent2}%)`;
}

/* ------------------------------- */
