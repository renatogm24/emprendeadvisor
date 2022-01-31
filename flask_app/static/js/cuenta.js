const optionsMenu = document.querySelectorAll(".menuProfileOpt");

function resetBtns() {
    optionsMenu.forEach(element => {
        element.classList.remove("bg-primary", "text-light");
        element.classList.add("bg-graytheme");
    });
}

for (const option of optionsMenu) {
    option.addEventListener("click", async(e) => {
        resetBtns();
        option.classList.remove("bg-graytheme");
        option.classList.add("bg-primary", "text-light");
        optionTxt = e.target.innerText;

        if (["Mi Perfil", "Mi Contraseña", "Mis Favoritos"].includes(optionTxt)) {
            const menu = document.querySelector(".profileMenu");
            menu.classList.add("d-none", "d-lg-block");
            const info = document.querySelector(".profileInfo");
            info.classList.remove("d-none");
            info.classList.add("d-block");

            profileForm = info.querySelector(".profileForm");
            if (optionTxt === "Mi Perfil") {

                const response = await fetch("http://127.0.0.1:5000/getUserSession");
                const data = await response.json();

                profileForm.innerHTML = "";
                const form = document.createElement("form");

                const first_name_label = document.createElement("label");
                first_name_label.classList.add("form-label", "mb-2");
                first_name_label.innerText = "Nombre:"
                form.appendChild(first_name_label);

                const first_name = document.createElement("input");
                first_name.value = data.first_name;
                first_name.name = "first_name";
                first_name.classList.add("form-control", "mb-2");
                form.appendChild(first_name);

                const last_name_label = document.createElement("label");
                last_name_label.classList.add("form-label", "mb-2");
                last_name_label.innerText = "Apellidos:"
                form.appendChild(last_name_label);

                const last_name = document.createElement("input");
                last_name.value = data.last_name;
                last_name.name = "last_name";
                last_name.classList.add("form-control", "mb-2");
                form.appendChild(last_name);

                const email_label = document.createElement("label");
                email_label.classList.add("form-label", "mb-2");
                email_label.innerText = "Correo:"
                form.appendChild(email_label);

                const email = document.createElement("input");
                email.value = data.email;
                email.name = "email";
                email.classList.add("form-control", "mb-2");
                form.appendChild(email);

                const button = document.createElement('input');
                button.classList.add("btn", "btn-altprimary", "text-light", "my-3");
                button.setAttribute('type', 'submit');
                button.value = "Actualizar";
                form.appendChild(button);

                form.addEventListener("submit", (e) => { updateProfile(e) });

                profileForm.appendChild(form);
            }

            if (optionTxt === "Mi Contraseña") {

                profileForm.innerHTML = "";
                const form = document.createElement("form");

                const password_actual_label = document.createElement("label");
                password_actual_label.classList.add("form-label", "mb-2");
                password_actual_label.innerText = "Contraseña actual:"
                form.appendChild(password_actual_label);

                const password_actual = document.createElement("input");
                password_actual.value = "";
                password_actual.name = "actual_password";
                password_actual.setAttribute('type', 'password');
                password_actual.classList.add("form-control", "mb-2");
                form.appendChild(password_actual);

                const password_label = document.createElement("label");
                password_label.classList.add("form-label", "mb-2");
                password_label.innerText = "Contraseña nueva:"
                form.appendChild(password_label);

                const password = document.createElement("input");
                password.value = "";
                password.name = "password";
                password.setAttribute('type', 'password');
                password.classList.add("form-control", "mb-2");
                form.appendChild(password);

                const password_repeat_label = document.createElement("label");
                password_repeat_label.classList.add("form-label", "mb-2");
                password_repeat_label.innerText = "Repetir contraseña nueva:"
                form.appendChild(password_repeat_label);

                const password_repeat = document.createElement("input");
                password_repeat.value = "";
                password_repeat.name = "repeat_password";
                password_repeat.setAttribute('type', 'password');
                password_repeat.classList.add("form-control", "mb-2");
                form.appendChild(password_repeat);

                const button = document.createElement('input');
                button.classList.add("btn", "btn-altprimary", "text-light", "my-3");
                button.setAttribute('type', 'submit');
                button.value = "Actualizar";
                form.appendChild(button);

                form.addEventListener("submit", (e) => { updatePassword(e) });

                profileForm.appendChild(form);
            }
        }
        if (optionTxt === "Cerrar Sesión") {
            window.location.href = "/logout";
        }
    })
}

async function updateProfile(event) {
    event.preventDefault();
    const errorLogin = document.querySelector(".errorLogin");
    const success = document.querySelector(".success");

    errorLogin.innerText = ""
    errorLogin.classList.remove("py-3");

    success.innerText = ""

    const form = new FormData(event.target);
    const response = await fetch("http://127.0.0.1:5000/updateProfile", {
        method: "POST",
        body: form,
    });
    const data = await response.json();
    if ("error" in data) {
        errorLogin.innerText = data.error;
        errorLogin.classList.add("py-3");
    } else if (data.updated) {
        success.innerText = "El usuario ha sido actualizado correctamente";
        success.classList.add("py-3");
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

    errorLogin.innerText = ""
    errorLogin.classList.remove("py-3");

    success.innerText = ""

    const form = new FormData(event.target);

    if(form.get("repeat_password")!==form.get("password") || form.get("password").length < 6){
        errorLogin.innerText = "Las contraseñas no coinciden o contiene menos de 6 caracteres";
        errorLogin.classList.add("py-3");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/updatePassword", {
        method: "POST",
        body: form,
    });
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


}