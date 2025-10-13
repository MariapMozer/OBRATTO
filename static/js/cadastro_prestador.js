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




// Máscara para telefone


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



// Preenchimento automático de endereço pelo CEP
document.getElementById('cep').addEventListener('blur', function() {
    const cep = this.value.replace(/\D/g, '');

    if (cep.length !== 8) {
        // Limpa os campos se o CEP for inválido
        document.getElementById('rua').value = '';
        document.getElementById('bairro').value = '';
        document.getElementById('cidade').value = '';
        return;
    }

    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                alert('CEP não encontrado!');
                document.getElementById('rua').value = '';
                document.getElementById('bairro').value = '';
                document.getElementById('cidade').value = '';
                return;
            }

            document.getElementById('rua').value = data.logradouro || '';
            document.getElementById('bairro').value = data.bairro || '';
            document.getElementById('cidade').value = data.localidade || '';
            document.getElementById('estado').value = data.uf || '';
        })
        .catch(err => {
            console.error('Erro ao consultar CEP:', err);
            alert('Erro ao consultar CEP.');
            document.getElementById('rua').value = '';
            document.getElementById('bairro').value = '';
            document.getElementById('cidade').value = '';
        });
});




// Submissão do formulário

document.getElementById('cadastroForm').addEventListener('submit', function(e) {
    if (!validarSecao(3)) {
        e.preventDefault();
        alert('Preencha todos os campos obrigatórios!');
        return;
    }

    // o formulário será enviado normalmente (rota definida no atributo "action" do form)
});


// animação de entrada
window.addEventListener('load', function() {
    document.querySelector('.cadastro-container').classList.add('fade-in-up');
});

// Máscara para CPF/CNPJ: só números, máximo 11 ou 14 dígitos
document.addEventListener('DOMContentLoaded', function() {
    const docInput = document.getElementById('documento');
    docInput.addEventListener('input', function(e) {
        let v = this.value.replace(/\D/g, '');
        if (v.length > 14) v = v.slice(0, 14);
        this.value = v;
    });

});

// Máscara para CPF/CNPJ: formata com pontos, traço e barra
document.addEventListener('DOMContentLoaded', function() {
    const docInput = document.getElementById('documento');
    docInput.addEventListener('input', function(e) {
        let v = this.value.replace(/\D/g, '');
        if (v.length > 14) v = v.slice(0, 14);

        // CPF: 000.000.000-00
        if (v.length <= 11) {
            v = v.replace(/(\d{3})(\d)/, '$1.$2');
            v = v.replace(/(\d{3})(\d)/, '$1.$2');
            v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        }
        // CNPJ: 00.000.000/0000-00
        else {
            v = v.replace(/^(\d{2})(\d)/, '$1.$2');
            v = v.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
            v = v.replace(/\.(\d{3})(\d)/, '.$1/$2');
            v = v.replace(/(\d{4})(\d{2})$/, '$1-$2');
        }
        this.value = v;
    });
});

// Máscara para CEP: 00000-000, só números, máximo 8 dígitos
document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.getElementById('cep');
    cepInput.addEventListener('input', function(e) {
        let v = this.value.replace(/\D/g, '');
        if (v.length > 8) v = v.slice(0, 8);
        if (v.length > 5) {
            v = v.replace(/(\d{5})(\d{1,3})/, '$1-$2');
        }
        this.value = v;
    });
});

