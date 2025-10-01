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
        alert('CEP inválido!');
        return;
    }


    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                alert('CEP não encontrado!');
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
            alert('Erro ao consultar CEP.');
        });
});




// Submissão do formulário


document.getElementById('cadastroForm').addEventListener('submit', function(e) {
    e.preventDefault();


    if (!validarSecao(3)) {
        alert('Preencha todos os campos obrigatórios!');
        return;
    }


    // Montar endereço completo antes de enviar
    const estado = document.getElementById('estado').value;
    const cidade = document.getElementById('cidade').value;
    const bairro = document.getElementById('bairro').value;
    const rua = document.getElementById('rua').value;
    const numero = document.getElementById('numero').value;
    const complemento = document.getElementById('complemento').value;


    const enderecoCompleto = `${rua}, ${numero} ${complemento ? '- ' + complemento : ''}, ${bairro}, ${cidade} - ${estado}`;
    document.getElementById('endereco').value = enderecoCompleto;


    // Aqui você pode adicionar a lógica para enviar os dados via AJAX ou form submit
    alert('Cadastro realizado com sucesso!');
});


// animação de entrada
window.addEventListener('load', function() {
    document.querySelector('.cadastro-container').classList.add('fade-in-up');
});
