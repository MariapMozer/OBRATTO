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

const cpfEl = document.getElementById('cpf');
if (cpfEl) {
    cpfEl.addEventListener('input', function (e) {
        console.log('e.target.value', e.target.value);
        let value = e.target.value
    if (!value) return;
    if (value.length > 14) value = value.slice(0, 14);
    value = value.replace(/\D/g, '');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    e.target.value = value;

    if (value.length >= 14) {
        console.log('e.target.value', e.target.value);

        fetch(`/api/verifica_cadastro_cliente/${e.target.value.replace('.', '').replace('.', '').replace('-', '')}`, {
            method: 'GET'
        })
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    alert('CPF já existe!');
                    return;
                }
            })
            .catch(err => {
                console.error('Erro ao consultar CPF:', JSON.stringify(err));
                alert('Erro ao consultar CPF.');
            });
    }
    })
}

// Máscara para telefone


const telefoneEl = document.getElementById('telefone');
if (telefoneEl) {
    telefoneEl.addEventListener('input', function (e) {
        let value = e.target.value.replace(/\D/g, '');
        value = value.replace(/(\d{2})(\d)/, '($1) $2');
        value = value.replace(/(\d{5})(\d)/, '$1-$2');
        e.target.value = value;
    });
}




// Validação de confirmação de senha


const confirmarSenhaEl = document.getElementById('confirmarSenha');
if (confirmarSenhaEl) {
    confirmarSenhaEl.addEventListener('input', function (e) {
        const senhaEl = document.getElementById('senha');
        const senha = senhaEl ? senhaEl.value : '';
        const confirmarSenha = e.target.value;

        if (senha !== confirmarSenha) {
            e.target.classList.add('is-invalid');
            e.target.classList.remove('is-valid');
        } else {
            e.target.classList.remove('is-invalid');
            e.target.classList.add('is-valid');
        }
    });
}




// Preenchimento automático de endereço pelo CEP


const cepEl = document.getElementById('cep');
if (cepEl) {
    cepEl.addEventListener('blur', function () {
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
                    const ruaEl = document.getElementById('rua');
                    const bairroEl = document.getElementById('bairro');
                    if (ruaEl) ruaEl.value = '';
                    if (bairroEl) bairroEl.value = '';
                    return;
                }

                const ruaEl = document.getElementById('rua');
                const bairroEl = document.getElementById('bairro');
                const cidadeEl = document.getElementById('cidade');
                const estadoEl = document.getElementById('estado');
                if (ruaEl) ruaEl.value = data.logradouro || '';
                if (bairroEl) bairroEl.value = data.bairro || '';
                if (cidadeEl) cidadeEl.value = data.localidade || '';
                if (estadoEl) estadoEl.value = data.uf || '';
            })
            .catch(err => {
                console.error('Erro ao consultar CEP:', err);
                alert('Erro ao consultar CEP.');
            });
    });
}




// Submissão do formulário

const cadastroFormEl = document.getElementById('cadastroForm');
if (cadastroFormEl) {
    cadastroFormEl.addEventListener('submit', function (e) {
        // prevenir submissão padrão e validar antes
        e.preventDefault();
        if (!validarSecao(3)) {
            alert('Preencha todos os campos obrigatórios!');
            return;
        }
        // se tudo OK, submete o formulário
        this.submit();
    });
}


// animação de entrada
window.addEventListener('load', function () {
    document.querySelector('.cadastro-container').classList.add('fade-in-up');
});
