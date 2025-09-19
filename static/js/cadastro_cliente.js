// Navegação entre seções
function proximaSecao(secaoAtual) {
    if (validarSecao(secaoAtual)) {
        document.getElementById('secao' + secaoAtual).classList.add('d-none');
        document.getElementById('secao' + (secaoAtual + 1)).classList.remove('d-none');

        // Atualizar indicador de progresso
        const steps = document.querySelectorAll('.progress-step');
        steps[secaoAtual - 1].classList.remove('active');
        steps[secaoAtual - 1].classList.add('completed');
        steps[secaoAtual].classList.add('active');
    }
}

function voltarSecao(secaoAtual) {
    document.getElementById('secao' + secaoAtual).classList.add('d-none');
    document.getElementById('secao' + (secaoAtual - 1)).classList.remove('d-none');

    // Atualizar indicador de progresso
    const steps = document.querySelectorAll('.progress-step');
    steps[secaoAtual - 1].classList.remove('active');
    steps[secaoAtual - 2].classList.remove('completed');
    steps[secaoAtual - 2].classList.add('active');
}

// Validação de seções
function validarSecao(secao) {
    let valido = true;
    const campos = document.querySelectorAll('#secao' + secao + ' [required]');

    campos.forEach(campo => {
        if (!campo.value.trim()) {
            campo.classList.add('is-invalid');
            valido = false;
        } else {
            campo.classList.remove('is-invalid');
            campo.classList.add('is-valid');
        }
    });

    return valido;
}

// Máscaras para CPF e telefone
document.getElementById('cpf').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

document.getElementById('telefone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{2})(\d)/, '($1) $2');
    value = value.replace(/(\d{5})(\d)/, '$1-$2');
    e.target.value = value;
});

// Validação de confirmação de senha
document.getElementById('confirmarSenha').addEventListener('input', function(e) {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = e.target.value;

    if (senha !== confirmarSenha) {
        e.target.classList.add('is-invalid');
    } else {
        e.target.classList.remove('is-invalid');
        e.target.classList.add('is-valid');
    }
});

// Submit do formulário
const cadastroForm = document.getElementById("cadastroForm");

cadastroForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    if (!validarSecao(3)) {
        alert("Preencha todos os campos obrigatórios!");
        return;
    }

    const formData = new FormData(cadastroForm);

    // Criar o campo 'endereco' concatenando os outros
    const enderecoCompleto = 
        formData.get('rua') + ', ' +
        formData.get('bairro') + ', ' +
        formData.get('cidade') + ' - ' +
        formData.get('estado');
    formData.set('endereco', enderecoCompleto);

    try {
        const resposta = await fetch('/cadastro/cliente', {
            method: 'POST',
            body: formData // envia como FormData
        });

        if (resposta.redirected) {
            window.location.href = resposta.url;
        } else {
            alert("Erro ao cadastrar!");
        }
    } catch (err) {
        console.error(err);
        alert("Falha de conexão com o servidor!");
    }
});

// Animação de entrada
window.addEventListener('load', function() {
    document.querySelector('.cadastro-container').classList.add('fade-in-up');
});