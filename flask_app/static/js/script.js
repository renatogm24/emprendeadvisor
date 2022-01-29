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

/* --------SLIDER -----------*/


let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let displayValOne = document.getElementById("range1");
let displayValTwo = document.getElementById("range2");
let minGap = 0;
let sliderTrack = document.querySelector(".slider-track");
let sliderMaxValue = document.getElementById("slider-1").max;

function slideOne(){
  if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
      sliderOne.value = parseInt(sliderTwo.value) - minGap;
  }
  displayValOne.textContent = (sliderOne.value/100).toFixed(1);
  fillColor();
}
function slideTwo(){
  if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
      sliderTwo.value = parseInt(sliderOne.value) + minGap;
  }
  displayValTwo.textContent =  (sliderTwo.value/100).toFixed(1);
  fillColor();
}
function fillColor(){
  percent1 = (sliderOne.value / sliderMaxValue) * 100;
  percent2 = (sliderTwo.value / sliderMaxValue) * 100;
  sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #192d4a ${percent1}% , #192d4a ${percent2}%, #dadae5 ${percent2}%)`;
}

/* ------------------------------- */

/* --------SLIDER2 -----------*/

window.onload = function(){
  slideOne();
  slideTwo();
  slide3();
  slide4();
  slide5();
  slide6();
}

let slider3 = document.getElementById("slider-3");
let slider4 = document.getElementById("slider-4");
let displayVal3 = document.getElementById("range3");
let displayVal4 = document.getElementById("range4");
let minGap2 = 0;
let sliderTrack2 = document.querySelectorAll(".slider-track")[1];
let sliderMaxValue2 = document.getElementById("slider-3").max;

function slide3(){
  if(parseInt(slider4.value) - parseInt(slider3.value) <= minGap2){
      slider3.value = parseInt(slider4.value) - minGap2;
  }
  displayVal3.textContent = slider3.value;
  fillColor2();
}

function slide4(){
  if(parseInt(slider4.value) - parseInt(slider3.value) <= minGap2){
      slider4.value = parseInt(slider3.value) + minGap2;
  }
  displayVal4.textContent = slider4.value;
  fillColor2();
}

function fillColor2(){
  percent1 = (slider3.value / sliderMaxValue2) * 100;
  percent2 = (slider4.value / sliderMaxValue2) * 100;
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
let sliderMaxValue3 = document.getElementById("slider-5").max;

function slide5(){
  if(parseInt(slider6.value) - parseInt(slider5.value) <= minGap3){
      slider5.value = parseInt(slider6.value) - minGap3;
  }
  displayVal5.textContent = slider5.value;
  fillColor3();
}

function slide6(){
  if(parseInt(slider6.value) - parseInt(slider5.value) <= minGap3){
      slider6.value = parseInt(slider5.value) + minGap3;
  }
  displayVal6.textContent = slider6.value;
  fillColor3();
}

function fillColor3(){
  percent1 = (slider5.value / sliderMaxValue3) * 100;
  percent2 = (slider6.value / sliderMaxValue3) * 100;
  sliderTrack3.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #192d4a ${percent1}% , #192d4a ${percent2}%, #dadae5 ${percent2}%)`;
}

/* ------------------------------- */