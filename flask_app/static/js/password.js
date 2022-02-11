const forgotForm = document.querySelector("#forgotForm");
forgotForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorForgot = document.querySelector(".errorForgot");
  errorForgot.innerText = "";
  errorForgot.classList.remove("py-3");
  const form = new FormData(forgotForm);
  const response = await fetch(
    "https://www.emprendeadvisor.com/reset/resetpassword",
    {
      method: "POST",
      body: form,
    }
  );
  const data = await response.json();
  if ("error" in data) {
    errorForgot.innerText = data.error;
    errorForgot.classList.add("py-3");
  } else if (data.updated) {
    const successForgot = document.querySelector(".successForgot");
    successForgot.innerText =
      "Se ha restablecido la clave, redirigiendo al inicio";
    successForgot.classList.add("py-3");
    setTimeout(() => {
      window.location.href = "/";
    }, 2000);
  }
});
