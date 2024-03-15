// UI components(visual actions) //////////////////////////

function toggle_password_visibility() {
    const password = document.getElementById("password");
    const hide_icon = document.getElementById("icon-1");
    if (password.type == "password") {
        password.type = "text";
        hide_icon.src = "https://img.icons8.com/material-outlined/24/visible--v1.png"
    }
    else {
        password.type = "password";
        hide_icon.src = "https://img.icons8.com/material-rounded/24/hide.png"
    }
}

function toggle_signup_password() {
    const password = document.getElementById("password-up");
    const hide_icon = document.getElementById("icon-2");
    if (password.type == "password") {
        password.type = "text";
        hide_icon.src = "https://img.icons8.com/material-outlined/24/visible--v1.png"
    }
    else {
        password.type = "password";
        hide_icon.src = "https://img.icons8.com/material-rounded/24/hide.png"
    }
}

function show_icon() {
    let passwordInput = document.getElementById("password");
    let usernameInput = document.getElementById("username");
    let login_btn = document.getElementById("login-btn");
    let login_span = document.getElementById("login-span");
    let hideIcon = document.getElementById('icon-1');

    if (passwordInput.value.length > 0) {
        hideIcon.hidden = false;
    } else {
        hideIcon.hidden = true;
        hideIcon.src = "https://img.icons8.com/material-rounded/24/hide.png"
        passwordInput.type = "password"
    }
    if (passwordInput.value.length > 0 && usernameInput.value.length > 0) {
        login_btn.removeAttribute("disabled")
        login_span.style.cursor = "pointer";
    }
    else {
        login_btn.disabled = true;
        login_span.style.cursor = "not-allowed";
    }

}

function show_icon_signup() {
    let usernameInput = document.getElementById("username-up");
    let passwordInput = document.getElementById("password-up");
    let signup_btn = document.getElementById("signup");
    let signup_span = document.getElementById("signup-span");
    let hideIcon = document.getElementById('icon-2');

    if (passwordInput.value.length > 0) {
        hideIcon.hidden = false;
    } else {
        hideIcon.hidden = true;
        hideIcon.src = "https://img.icons8.com/material-rounded/24/hide.png";
        passwordInput.type = "password";
    }
    if (passwordInput.value.length > 0 && usernameInput.value.length > 0) {
        signup_btn.removeAttribute("disabled")
        signup_span.style.cursor = "pointer";
    }
    else {
        signup_btn.disabled = true;
        signup_span.style.cursor = "not-allowed";
    }
}

function signup_dialog() {
    const signup_window = document.getElementById("signup-dialog");
    const closeBtn = document.getElementById("closeBtn");
    data = {}
    if (!signup_window.open) {
        signup_window.showModal();
    }
    closeBtn.addEventListener('click', () => {
        document.getElementById("response-message-up").innerText = "";
        document.getElementById("password-up").value = "";
        document.getElementById("username-up").value = "";
        document.getElementById("icon-2").hidden = true;
        signup_window.close();
    })

}

function turn_light() {
    let bod = document.getElementById("bod");
    let heading = document.getElementById("sms-head");
    let auth_box = document.getElementById("auth-base");
    let signup_box = document.getElementById("signup-dialog");
    let checkbox = document.getElementById("checkbox");

    if (checkbox.checked) {
        bod.className = "light-bod";
        heading.className = "smp-light display-2";
        auth_box.className = "auth-base-light";
        signup_box.className = "signup-dialog-light";
    }
    else {
        bod.className = "dark-bod";
        heading.className = "smp-dark display-2";
        auth_box.className = "auth-base-dark";
        signup_box.className = "signup-dialog-dark";    
    }
}

// Working with backend servers //////////////////////////////////////////////////////////
function authenticate_login() {
    const form = document.getElementById("login-form");
    const responseMessage = document.getElementById("responseMessage");
    const payload = {
        username: form.elements['username'].value,
        password: form.elements['password'].value
    }

    const json_data = JSON.stringify(payload);

    $.ajax({
        type: "POST",
        url: "http://localhost:5000/login",
        data: json_data,
        contentType: "application/json",
        headers: { authorization: "Bearer " + response?.token },
        success: function (response) {
            if (response.status_code == 201) {
                responseMessage.innerText = response?.message.slice(0, 18);
                console.log(response?.message.slice(0, 18))

                setTimeout(function () {
                    responseMessage.innerText += response?.message.slice(18, 28);
                    console.log(response?.message.slice(18, 28))
                }, 500);

                setTimeout(function () {
                    responseMessage.innerText += response?.message.slice(27, 39);
                    console.log(response?.message.slice(27, 39));
                }, 1000);

                setTimeout(function () {
                    responseMessage.innerText += response?.message.slice(38, 53);
                    console.log(response?.message.slice(38, 53));
                }, 1500);

                setTimeout(function () {
                    window.location.replace("http://localhost:5500/static/html/homepage.html");    
                    localStorage.setItem('token', response?.token);
                    localStorage.setItem('WWW-Authenticate', response["WWW-Authenticate"])
                }, 2000);

            }
            else if (response.status_code == 403) {
                responseMessage.innerText = response?.message;
                responseMessage.style.color = "rgba(227, 3, 21, 1)";
                responseMessage.style.backgroundColor = "rgba(227, 21, 21, 0.307)";
                responseMessage.style.borderRadius = "4px";
                responseMessage.style.paddingLeft = "1px";
                localStorage.setItem('WWW-Authenticate', response["WWW-Authenticate"]);
                localStorage.removeItem("token");
            }
        },
        error: function (response) {
            console.log(response);
        },
    });
}


function signup_submit() {

    let form = document.getElementById("signup-form");
    let responseMessage = document.getElementById("response-message-up");
    const payload = {
        username: form.elements['username-up'].value,
        password: form.elements['password-up'].value
    }
    const json_data = JSON.stringify(payload)
    console.log(json_data)
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/users",
        contentType: "application/json",
        data: json_data,
        success: function (response) {
            responseMessage.textContent = response?.message;
        },
        error: function (response) {
            errorMessage = ""
            if (response?.responseJSON?.username?.[0] != undefined) {
                errorMessage += response?.responseJSON?.username?.[0];
            } else if (response?.responseJSON?.password?.[0] != undefined) {
                errorMessage += response?.responseJSON?.password?.[0];
            }
            responseMessage.textContent = "Error occured 101: " + errorMessage;
        },

    })

}





