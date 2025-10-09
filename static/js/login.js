document.addEventListener("DOMContentLoaded", function() {
    console.log("login.js loaded (v2)");
    const loginForm = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const senhaInput = document.getElementById("senha");
    const toggleSenha = document.getElementById("toggleSenha");
    const lembrarMeCheckbox = document.getElementById("lembrarMe");
    
    setTimeout(() => {
        document.querySelector(".login-container").classList.add("fade-in-up");
    }, 100);
    
   if (toggleSenha) {
        toggleSenha.addEventListener("click", function() {
            const tipo = senhaInput.getAttribute("type") === "password" ? "text" : "password";
            senhaInput.setAttribute("type", tipo);

            const icon = this.querySelector("i");
            if (tipo === "text") {
                icon.classList.remove("bi-eye-fill");
                icon.classList.add("bi-eye-slash-fill");
            } else {
                icon.classList.remove("bi-eye-slash-fill");
                icon.classList.add("bi-eye-fill");
            }
        });
    }
    
    emailInput.addEventListener("input", function() {
        validarCampo(this);
    });
    
    senhaInput.addEventListener("input", function() {
        validarCampo(this);
    });
    
    loginForm.addEventListener("submit", function(e) {
        if (!validarFormulario()) {
            e.preventDefault(); // impede envio apenas se inválido
        }
    });


    
    carregarDadosSalvos();
});

function validarCampo(campo) {
    const valor = campo.value.trim();
    
    if (valor === "") {
        campo.classList.add("is-invalid");
        campo.classList.remove("is-valid");
        return false;
    } else {
        campo.classList.remove("is-invalid");
        campo.classList.add("is-valid");
        return true;
    }
}

function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validarUsuario(valor) {
    const texto = valor.trim();
    
    if (texto.length < 3) {
        return false;
    }
    
    if (texto.includes("@")) {
        return validarEmail(texto);
    }
    
    return true;
}

function validarFormulario() {
    const email = document.getElementById("email");
    const senha = document.getElementById("senha");
    let valido = true;
    
    if (!validarCampo(email) || !validarUsuario(email.value)) {
        email.classList.add("is-invalid");
        valido = false;
    }
    
    if (!validarCampo(senha) || senha.value.length < 6) {
        senha.classList.add("is-invalid");
        valido = false;
    }
    
    return valido;
}

async function realizarLogin() {
    const btnLogin = document.querySelector(".btn-login");
    const textoOriginal = btnLogin.innerHTML;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    const lembrarMe = document.getElementById("lembrarMe").checked;

    btnLogin.innerHTML = "<i class=\"bi bi-hourglass-split me-2\"></i>Entrando...";
    btnLogin.disabled = true;

    try {
        // Criando FormData para enviar como formulário tradicional
        const formData = new FormData();
        formData.append("email", email);  // rota espera "email"
        formData.append("senha", senha);

        const response = await fetch("/login", {
            method: "POST",
            body: formData,
            // important: include credentials so the session cookie set by FastAPI is stored
            credentials: 'same-origin',
            // prefer receiving the final redirected URL
            redirect: 'follow',
            // mark as AJAX so backend may return JSON with redirect target
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        });

        // Debug logs: status and redirected info
        console.log("Login fetch response: status=", response.status, "ok=", response.ok, "redirected=", response.redirected);
        try {
            console.log("Response headers (set-cookie present?):", response.headers.get('set-cookie'));
        } catch (e) {
            console.log("Unable to read set-cookie from response headers in JS (browser blocks it).", e);
        }

        // Se o backend retornou JSON (fluxo AJAX), usa o campo redirect
        const contentType = response.headers.get('content-type') || '';
        if (contentType.indexOf('application/json') !== -1) {
            const data = await response.json().catch(() => null);
            if (data && data.success && data.redirect) {
                if (lembrarMe) salvarDados(email);
                else limparDadosSalvos();
                window.location.href = data.redirect;
                return;
            }
        }

        if (response.redirected) {
            // Se login deu certo, o FastAPI redireciona
            if (lembrarMe) salvarDados(email);
            else limparDadosSalvos();

            window.location.href = response.url; 
            return;
        } else {
            // Se não houve redirect, provavelmente veio a página de login com erro
            mostrarErro("Usuário ou senha inválidos.");
            btnLogin.innerHTML = textoOriginal;
            btnLogin.disabled = false;
        }
    } catch (error) {
        console.error("Erro ao realizar login:", error);
        mostrarErro("Ocorreu um erro ao tentar fazer login. Tente novamente.");
        btnLogin.innerHTML = textoOriginal;
        btnLogin.disabled = false;
    }
}

function mostrarSucesso() {
    const feedback = document.createElement("div");
    feedback.className = "login-success";
    feedback.innerHTML = `
        <i class="bi bi-check-circle-fill"></i>
        Login realizado com sucesso!
    `;
    
    feedback.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 8px 20px rgba(40, 167, 69, 0.3);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 8px;
    `;
    
    document.body.appendChild(feedback);
    
    setTimeout(() => {
        feedback.style.animation = "slideOutRight 0.3s ease-in";
        setTimeout(() => {
            if (document.body.contains(feedback)) {
                document.body.removeChild(feedback);
            }
        }, 300);
    }, 3000);
}

function mostrarErro(mensagem) {
    const feedback = document.createElement("div");
    feedback.className = "login-error";
    feedback.innerHTML = `
        <i class="bi bi-exclamation-triangle-fill"></i>
        ${mensagem}
    `;
    
    feedback.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 8px 20px rgba(220, 53, 69, 0.3);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 8px;
    `;
    
    document.body.appendChild(feedback);
    
    setTimeout(() => {
        feedback.style.animation = "slideOutRight 0.3s ease-in";
        setTimeout(() => {
            if (document.body.contains(feedback)) {
                document.body.removeChild(feedback);
            }
        }, 300);
    }, 3000);
}

function salvarDados(email) {
    localStorage.setItem("obratto_email", email);
    localStorage.setItem("obratto_lembrar", "true");
}

function limparDadosSalvos() {
    localStorage.removeItem("obratto_email");
    localStorage.removeItem("obratto_lembrar");
}

function carregarDadosSalvos() {
    const emailSalvo = localStorage.getItem("obratto_email");
    const lembrarSalvo = localStorage.getItem("obratto_lembrar");
    
    if (emailSalvo && lembrarSalvo === "true") {
        document.getElementById("email").value = emailSalvo;
        document.getElementById("lembrarMe").checked = true;
    }
}

document.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        const activeElement = document.activeElement;
        
        if (activeElement.id === "email") {
            document.getElementById("senha").focus();
        } else if (activeElement.id === "senha") {
            document.getElementById("loginForm").dispatchEvent(new Event("submit"));
        }
    }
});

const style = document.createElement("style");
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .form-control:focus {
        animation: focusGlow 0.3s ease-out;
    }
    
    @keyframes focusGlow {
        0% {
            box-shadow: 0 0 0 0 rgba(232, 137, 75, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(232, 137, 75, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(232, 137, 75, 0);
        }
    }
`;
document.head.appendChild(style);
