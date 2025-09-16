document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const usuarioInput = document.getElementById("usuario");
    const senhaInput = document.getElementById("senha");
    const toggleSenha = document.getElementById("toggleSenha");
    const lembrarMeCheckbox = document.getElementById("lembrarMe");
    
    setTimeout(() => {
        document.querySelector(".login-container").classList.add("fade-in-up");
    }, 100);
    
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
    
    usuarioInput.addEventListener("input", function() {
        validarCampo(this);
    });
    
    senhaInput.addEventListener("input", function() {
        validarCampo(this);
    });
    
    loginForm.addEventListener("submit", function(e) {
        e.preventDefault();
        
        if (validarFormulario()) {
            realizarLogin();
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


function validarUsuario(usuario) {
    const valor = usuario.trim();
    
    if (valor.length < 3) {
        return false;
    }
    
    if (valor.includes("@")) {
        return validarEmail(valor);
    }
    
    return true;
}

function validarFormulario() {
    const usuario = document.getElementById("usuario");
    const senha = document.getElementById("senha");
    let valido = true;
    
    if (!validarCampo(usuario) || !validarUsuario(usuario.value)) {
        usuario.classList.add("is-invalid");
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
    const usuario = document.getElementById("usuario").value;
    const senha = document.getElementById("senha").value;
    const lembrarMe = document.getElementById("lembrarMe").checked;
    
    btnLogin.innerHTML = "<i class=\"bi bi-hourglass-split me-2\"></i>Entrando...";
    btnLogin.disabled = true;
    
    try {
        // AQUI VOCÊ DEVE FAZER A CHAMADA REAL PARA SUA API DE LOGIN
        // Exemplo usando fetch (você precisará adaptar para sua API):
        // const response = await fetch("/api/login", {
        //     method: "POST",
        //     headers: {
        //         "Content-Type": "application/json",
        //     },
        //     body: JSON.stringify({ usuario, senha }),
        // });
        
        // const data = await response.json();
        
        // if (response.ok) {
        //     // Login bem-sucedido
        //     if (lembrarMe) {
        //         salvarDados(usuario);
        //     } else {
        //         limparDadosSalvos();
        //     }
        //     mostrarSucesso();
        //     setTimeout(() => {
        //         window.location.href = "/dashboard"; // Redirecionar para o dashboard
        //     }, 2000);
        // } else {
        //     // Login falhou
        //     mostrarErro(data.message || "Credenciais inválidas.");
        //     btnLogin.innerHTML = textoOriginal;
        //     btnLogin.disabled = false;
        // }

        // --- SIMULAÇÃO TEMPORÁRIA PARA TESTE (REMOVER EM PRODUÇÃO) ---
        await new Promise(resolve => setTimeout(resolve, 1500)); // Simula delay da rede
        if (usuario === "teste@teste.com" && senha === "123456") {
            if (lembrarMe) {
                salvarDados(usuario);
            } else {
                limparDadosSalvos();
            }
            mostrarSucesso();
            setTimeout(() => {
                window.location.href = "/dashboard";
            }, 2000);
        } else {
            mostrarErro("Usuário ou senha inválidos.");
            btnLogin.innerHTML = textoOriginal;
            btnLogin.disabled = false;
        }
        // --- FIM DA SIMULAÇÃO TEMPORÁRIA ---

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

function salvarDados(usuario) {
    localStorage.setItem("obratto_usuario", usuario);
    localStorage.setItem("obratto_lembrar", "true");
}

function limparDadosSalvos() {
    localStorage.removeItem("obratto_usuario");
    localStorage.removeItem("obratto_lembrar");
}

function carregarDadosSalvos() {
    const usuarioSalvo = localStorage.getItem("obratto_usuario");
    const lembrarSalvo = localStorage.getItem("obratto_lembrar");
    
    if (usuarioSalvo && lembrarSalvo === "true") {
        document.getElementById("usuario").value = usuarioSalvo;
        document.getElementById("lembrarMe").checked = true;
    }
}

document.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        const activeElement = document.activeElement;
        
        if (activeElement.id === "usuario") {
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
