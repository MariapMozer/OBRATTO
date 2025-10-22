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

// máscara para CPF

document.getElementById('cpf').addEventListener('input', function (e) {
    let value = e.target.value;
    if (!value) return;
    if (value.length > 14) value = value.slice(0, 14);
    value = value.replace(/\D/g, '');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;
});

// Máscara para telefone


document.getElementById('telefone').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{2})(\d)/, '($1) $2');
    value = value.replace(/(\d{5})(\d)/, '$1-$2');
    e.target.value = value;
});




// Validação de confirmação de senha


document.getElementById('confirmarSenha').addEventListener('input', function (e) {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = e.target.value;


    if (senha !== confirmarSenha) {
        e.target.classList.add('is-invalid');
    } else {
        e.target.classList.remove('is-invalid');
        e.target.classList.add('is-valid');
    }
});




// Preenchimento automático de endereço pelo CEP


document.getElementById('cep').addEventListener('blur', function () {
    const cep = this.value.replace(/\D/g, '');


    if (cep.length !== 8) {
        return;
    }


    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                document.getElementById('rua').value = '';
                document.getElementById('bairro').value = '';
                return;
            }


            document.getElementById('rua').value = data.logradouro || '';
            document.getElementById('bairro').value = data.bairro || '';
            document.getElementById('cidade').value = data.localidade || '';
            document.getElementById('estado').value = data.uf || '';
        })
        .catch(err => {
            console.error('Erro ao consultar CEP:', err);
        });
});




// Submissão do formulário


document.getElementById('cadastroForm').addEventListener('submit', function (e) {
    // Validar seção 3 antes de submeter
    if (!validarSecao(3)) {
        e.preventDefault();
        return;
    }

    // Permitir submissão normal do formulário
});


// animação de entrada
window.addEventListener('load', function () {
    document.querySelector('.cadastro-container').classList.add('fade-in-up');
});
