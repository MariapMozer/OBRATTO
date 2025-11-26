// ===============================
// Navegação entre seções
// ===============================

function proximaSecao(secaoAtual) {
    if (validarSecao(secaoAtual)) {
        document.getElementById('secao' + secaoAtual).classList.add('d-none');
        document.getElementById('secao' + (secaoAtual + 1)).classList.remove('d-none');

        // Atualizar indicador de progresso
        const steps = document.querySelectorAll('.progress-step');
        steps[secaoAtual - 1].classList.remove('active');
        steps[secaoAtual - 1].classList.add('completed');
        steps[secaoAtual].classList.add('active');
    } else {
        showToast('Por favor, preencha todos os campos obrigatórios corretamente.', 'warning');
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

// ===============================
// Validação de seções
// ===============================

function validarSecao(secao) {
    let valido = true;
    const campos = document.querySelectorAll('#secao' + secao + ' [required]');
    const erros = [];

    campos.forEach(campo => {
        // Remove validações anteriores
        campo.classList.remove('is-invalid', 'is-valid');

        if (!campo.value.trim()) {
            campo.classList.add('is-invalid');
            const label = campo.previousElementSibling?.textContent || campo.getAttribute('placeholder');
            erros.push(`O campo ${label.replace('*', '').trim()} é obrigatório.`);
            valido = false;
        } else {
            // Validações específicas por tipo de campo
            switch(campo.id) {
                case 'cpf':
                    if (!validarCPF(campo.value)) {
                        campo.classList.add('is-invalid');
                        erros.push('CPF inválido.');
                        valido = false;
                    }
                    break;
                case 'email':
                    if (!validarEmail(campo.value)) {
                        campo.classList.add('is-invalid');
                        erros.push('E-mail inválido.');
                        valido = false;
                    }
                    break;
                case 'senha':
                    if (!validarSenha(campo.value)) {
                        campo.classList.add('is-invalid');
                        erros.push('A senha deve ter pelo menos 8 caracteres, incluindo letras e números.');
                        valido = false;
                    }
                    break;
                case 'confirmarSenha':
                    if (campo.value !== document.getElementById('senha').value) {
                        campo.classList.add('is-invalid');
                        erros.push('As senhas não coincidem.');
                        valido = false;
                    }
                    break;
                case 'telefone':
                    if (!validarTelefone(campo.value)) {
                        campo.classList.add('is-invalid');
                        erros.push('Telefone inválido.');
                        valido = false;
                    }
                    break;
            }

            if (valido) {
                campo.classList.add('is-valid');
            }
        }
    });

    if (erros.length > 0) {
        showToast(erros.join('<br>'), 'warning');
    }

    return valido;
}

// ===============================
// Máscaras de entrada
// ===============================

// CPF
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

// Telefone
document.getElementById('telefone').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{2})(\d)/, '($1) $2');
    value = value.replace(/(\d{5})(\d)/, '$1-$2');
    e.target.value = value;
});

// ===============================
// Validação de confirmação de senha
// ===============================

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

// ===============================
// Preenchimento automático do endereço
// ===============================

document.getElementById('cep').addEventListener('blur', function () {
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

// ===============================
// Funções de Validação
// ===============================

function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;

    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let digito = 11 - (soma % 11);
    if (digito > 9) digito = 0;
    if (digito != parseInt(cpf.charAt(9))) return false;

    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    digito = 11 - (soma % 11);
    if (digito > 9) digito = 0;
    if (digito != parseInt(cpf.charAt(10))) return false;

    return true;
}

function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validarSenha(senha) {
    return senha.length >= 8 && /[A-Za-z]/.test(senha) && /[0-9]/.test(senha);
}

function validarTelefone(telefone) {
    const tel = telefone.replace(/\D/g, '');
    return tel.length >= 10 && tel.length <= 11;
}

// ===============================
// Submissão do formulário
// ===============================

window.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("cadastroForm");
    if (!form) {
        console.error("Formulário de cadastro não encontrado!");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (!validarSecao(3)) {
            return;
        }

        // Cache the submit button and its original text
        const submitBtn = form.querySelector('button[type="submit"]');
        if (!submitBtn) {
            console.error("Botão de submit não encontrado!");
            return;
        }
        const originalText = submitBtn.innerHTML;

        try {
            const formData = new FormData(form);

            // Mostra loading
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i> Aguarde...';

            const response = await fetch(form.action, {
                method: form.method,
                body: formData
            });

            // Tenta processar a resposta
            let data;
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                const text = await response.text();
                // Se for redirecionamento, segue
                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }
                // Senão, considera erro
                throw new Error('Resposta inválida do servidor');
            }

            // Processa resposta JSON
            if (response.ok) {
                showToast('Cadastro realizado com sucesso!', 'success');
                setTimeout(() => {
                    window.location.href = '/entrar';
                }, 2000);
            } else {
                // Erros de validação do servidor
                if (data.erros) {
                    Object.entries(data.erros).forEach(([campo, mensagem]) => {
                        const input = form.querySelector(`[name="${campo}"]`);
                        if (input) {
                            input.classList.add('is-invalid');
                            const feedback = input.nextElementSibling;
                            if (feedback && feedback.classList.contains('invalid-feedback')) {
                                feedback.textContent = mensagem;
                            }
                        }
                    });
                    showToast('Por favor, corrija os erros indicados.', 'warning');
                } else if (data.message) {
                    showToast(data.message, 'error');
                } else {
                    throw new Error('Erro ao processar cadastro');
                }
            }
        } catch (error) {
            console.error('Erro no cadastro:', error);
            showToast(
                'Ocorreu um erro interno. Por favor, tente novamente mais tarde.',
                'error'
            );
        } finally {
            // Restaura botão
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }
    });
});

// ===============================
// Animação de entrada
// ===============================

window.addEventListener('load', function () {
    document.querySelector('.cadastro-container').classList.add('fade-in-up');
});

// ===============================
// Exporta funções para o HTML
// ===============================
window.proximaSecao = proximaSecao;
window.voltarSecao = voltarSecao;
