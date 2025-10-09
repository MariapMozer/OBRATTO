/**
 * Funcionalidades avançadas para o formulário de cadastro de administradores
 */

class AdminForm {
    constructor() {
        this.form = document.getElementById('adminForm');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupValidations();
        this.setupMasks();
        this.setupPermissionPresets();
        this.setupFormSubmission();
    }

    setupEventListeners() {
        // Validação em tempo real
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });

        // Confirmação de senha em tempo real
        const senhaInput = document.getElementById('senha');
        const confirmarSenhaInput = document.getElementById('confirmarSenha');
        
        senhaInput.addEventListener('input', () => {
            this.checkPasswordStrength(senhaInput.value);
            this.validatePasswordMatch();
        });
        
        confirmarSenhaInput.addEventListener('input', () => {
            this.validatePasswordMatch();
        });

        // Mudança de nível de acesso
        const nivelAcessoSelect = document.getElementById('nivelAcesso');
        nivelAcessoSelect.addEventListener('change', () => {
            this.setPermissionsByLevel(nivelAcessoSelect.value);
        });
    }

    setupValidations() {
        // Validação de email
        const emailInput = document.getElementById('email');
        emailInput.addEventListener('blur', () => {
            if (emailInput.value) {
                this.validateEmail(emailInput.value);
            }
        });

        // Validação de CPF
        const cpfInput = document.getElementById('cpf');
        cpfInput.addEventListener('blur', () => {
            if (cpfInput.value) {
                this.validateCPF(cpfInput.value);
            }
        });
    }

    setupMasks() {
        // Máscara para CPF
        const cpfInput = document.getElementById('cpf');
        cpfInput.addEventListener('input', (e) => {
            e.target.value = this.applyCPFMask(e.target.value);
        });

        // Máscara para telefone
        const telefoneInput = document.getElementById('telefone');
        telefoneInput.addEventListener('input', (e) => {
            e.target.value = this.applyPhoneMask(e.target.value);
        });
    }

    setupPermissionPresets() {
        const presets = {
            'admin_master': [
                'usuarios_visualizar', 'usuarios_editar', 'usuarios_excluir',
                'conteudo_criar', 'conteudo_editar', 'conteudo_excluir',
                'financeiro_visualizar', 'financeiro_editar',
                'sistema_configurar', 'sistema_logs'
            ],
            'admin_geral': [
                'usuarios_visualizar', 'usuarios_editar',
                'conteudo_criar', 'conteudo_editar',
                'sistema_logs'
            ],
            'admin_moderador': [
                'usuarios_visualizar',
                'conteudo_editar', 'conteudo_excluir'
            ],
            'admin_suporte': [
                'usuarios_visualizar'
            ],
            'admin_financeiro': [
                'financeiro_visualizar', 'financeiro_editar'
            ]
        };

        this.permissionPresets = presets;
    }

    setupFormSubmission() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmission();
        });
    }

    // Validações
    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        switch (field.type) {
            case 'email':
                if (value && !this.isValidEmail(value)) {
                    isValid = false;
                    message = 'Email inválido';
                }
                break;
            case 'password':
                if (field.id === 'senha' && value.length < 8) {
                    isValid = false;
                    message = 'Senha deve ter pelo menos 8 caracteres';
                }
                break;
            case 'tel':
                if (value && !this.isValidPhone(value)) {
                    isValid = false;
                    message = 'Telefone inválido';
                }
                break;
        }

        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'Campo obrigatório';
        }

        this.setFieldValidation(field, isValid, message);
        return isValid;
    }

    validateEmail(email) {
        const isValid = this.isValidEmail(email);
        const emailInput = document.getElementById('email');
        
        if (isValid) {
            // Verificar se email já existe (simulação)
            this.checkEmailExists(email).then(exists => {
                if (exists) {
                    this.setFieldValidation(emailInput, false, 'Este email já está cadastrado');
                } else {
                    this.setFieldValidation(emailInput, true);
                }
            });
        } else {
            this.setFieldValidation(emailInput, false, 'Email inválido');
        }
    }

    validateCPF(cpf) {
        const isValid = this.isValidCPF(cpf);
        const cpfInput = document.getElementById('cpf');
        this.setFieldValidation(cpfInput, isValid, isValid ? '' : 'CPF inválido');
    }

    validatePasswordMatch() {
        const senha = document.getElementById('senha').value;
        const confirmarSenha = document.getElementById('confirmarSenha').value;
        const passwordMatch = document.getElementById('passwordMatch');
        const confirmarSenhaInput = document.getElementById('confirmarSenha');

        if (confirmarSenha.length > 0) {
            if (senha === confirmarSenha) {
                passwordMatch.textContent = '✓ Senhas coincidem';
                passwordMatch.style.color = '#28a745';
                confirmarSenhaInput.classList.remove('is-invalid');
                confirmarSenhaInput.classList.add('is-valid');
                return true;
            } else {
                passwordMatch.textContent = '✗ Senhas não coincidem';
                passwordMatch.style.color = '#dc3545';
                confirmarSenhaInput.classList.remove('is-valid');
                confirmarSenhaInput.classList.add('is-invalid');
                return false;
            }
        } else {
            passwordMatch.textContent = '';
            confirmarSenhaInput.classList.remove('is-valid', 'is-invalid');
            return true;
        }
    }

    checkPasswordStrength(password) {
        const strengthBar = document.getElementById('strengthBar');
        const strengthText = document.getElementById('strengthText');
        
        let strength = 0;
        let text = '';
        
        if (password.length >= 8) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;
        
        strengthBar.className = 'strength-fill';
        
        switch(strength) {
            case 0:
            case 1:
                strengthBar.classList.add('strength-weak');
                text = 'Senha muito fraca';
                break;
            case 2:
                strengthBar.classList.add('strength-fair');
                text = 'Senha fraca';
                break;
            case 3:
                strengthBar.classList.add('strength-good');
                text = 'Senha boa';
                break;
            case 4:
            case 5:
                strengthBar.classList.add('strength-strong');
                text = 'Senha forte';
                break;
        }
        
        strengthText.textContent = text;
        return strength;
    }

    // Máscaras
    applyCPFMask(value) {
        value = value.replace(/\D/g, '');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        return value;
    }

    applyPhoneMask(value) {
        value = value.replace(/\D/g, '');
        if (value.length <= 10) {
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{4})(\d)/, '$1-$2');
        } else {
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
        }
        return value;
    }

    // Validadores
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    isValidCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        
        if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) {
            return false;
        }
        
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf.charAt(i)) * (10 - i);
        }
        
        let remainder = (sum * 10) % 11;
        if (remainder === 10 || remainder === 11) remainder = 0;
        if (remainder !== parseInt(cpf.charAt(9))) return false;
        
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf.charAt(i)) * (11 - i);
        }
        
        remainder = (sum * 10) % 11;
        if (remainder === 10 || remainder === 11) remainder = 0;
        return remainder === parseInt(cpf.charAt(10));
    }

    isValidPhone(phone) {
        const phoneRegex = /^\(\d{2}\) \d{4,5}-\d{4}$/;
        return phoneRegex.test(phone);
    }

    // Utilitários
    setFieldValidation(field, isValid, message = '') {
        const feedback = field.parentNode.querySelector('.invalid-feedback') || 
                        field.parentNode.querySelector('.valid-feedback');
        
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            if (feedback) feedback.remove();
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            
            if (!feedback && message) {
                const feedbackDiv = document.createElement('div');
                feedbackDiv.className = 'invalid-feedback';
                feedbackDiv.textContent = message;
                field.parentNode.appendChild(feedbackDiv);
            } else if (feedback && message) {
                feedback.textContent = message;
                feedback.className = 'invalid-feedback';
            }
        }
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) feedback.remove();
    }

    setPermissionsByLevel(level) {
        const checkboxes = document.querySelectorAll('input[name="permissoes[]"]');
        
        // Limpar todas as permissões
        checkboxes.forEach(cb => cb.checked = false);
        
        // Aplicar permissões do preset
        if (this.permissionPresets[level]) {
            this.permissionPresets[level].forEach(permission => {
                const checkbox = document.getElementById(`perm_${permission}`);
                if (checkbox) checkbox.checked = true;
            });
        }
    }

    async checkEmailExists(email) {
        // Simulação de verificação de email existente
        // Em um ambiente real, isso seria uma chamada para a API
        return new Promise(resolve => {
            setTimeout(() => {
                // Simular alguns emails já existentes
                const existingEmails = ['admin@obratto.com', 'master@obratto.com'];
                resolve(existingEmails.includes(email.toLowerCase()));
            }, 500);
        });
    }

    validateForm() {
        const inputs = this.form.querySelectorAll('input[required], select[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        // Validações específicas
        if (!this.validatePasswordMatch()) {
            isValid = false;
        }

        const senha = document.getElementById('senha').value;
        if (this.checkPasswordStrength(senha) < 2) {
            this.setFieldValidation(document.getElementById('senha'), false, 'Senha muito fraca');
            isValid = false;
        }

        return isValid;
    }

    async handleFormSubmission() {
        const submitBtn = this.form.querySelector('button[type="submit"]');
        
        // Mostrar loading
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            if (!this.validateForm()) {
                throw new Error('Por favor, corrija os erros no formulário');
            }

            // Coletar dados do formulário
            const formData = new FormData(this.form);
            const data = Object.fromEntries(formData.entries());
            
            // Coletar permissões selecionadas
            const permissoes = Array.from(document.querySelectorAll('input[name="permissoes[]"]:checked'))
                .map(cb => cb.value);
            data.permissoes = permissoes;

            // Simular envio para API
            await this.submitToAPI(data);
            
            // Mostrar sucesso
            this.showMessage('Administrador cadastrado com sucesso!', 'success');
            
            // Resetar formulário após sucesso
            setTimeout(() => {
                this.form.reset();
                this.clearAllValidations();
            }, 2000);

        } catch (error) {
            this.showMessage(error.message, 'error');
        } finally {
            // Remover loading
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    }

    async submitToAPI(data) {
        // Simulação de envio para API
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // Simular erro ocasional
                if (Math.random() < 0.1) {
                    reject(new Error('Erro interno do servidor. Tente novamente.'));
                } else {
                    resolve({ success: true, id: Date.now() });
                }
            }, 2000);
        });
    }

    showMessage(message, type) {
        // Criar container de mensagens se não existir
        let container = document.querySelector('.message-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'message-container';
            document.body.appendChild(container);
        }

        // Criar alerta
        const alert = document.createElement('div');
        alert.className = `alert message-alert alert-${type === 'success' ? 'success' : 'danger'}`;
        alert.innerHTML = `
            <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;

        container.appendChild(alert);

        // Remover automaticamente após 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    clearAllValidations() {
        const inputs = this.form.querySelectorAll('.is-valid, .is-invalid');
        inputs.forEach(input => {
            input.classList.remove('is-valid', 'is-invalid');
        });

        const feedbacks = this.form.querySelectorAll('.invalid-feedback, .valid-feedback');
        feedbacks.forEach(feedback => feedback.remove());

        // Limpar indicadores de senha
        document.getElementById('passwordMatch').textContent = '';
        document.getElementById('strengthText').textContent = 'A senha deve ter pelo menos 8 caracteres';
        document.getElementById('strengthBar').className = 'strength-fill';
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    new AdminForm();
});

// Utilitários globais
window.AdminFormUtils = {
    // Função para exportar dados do formulário
    exportFormData() {
        const form = document.getElementById('adminForm');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        const permissoes = Array.from(document.querySelectorAll('input[name="permissoes[]"]:checked'))
            .map(cb => cb.value);
        data.permissoes = permissoes;
        
        return data;
    },

    // Função para importar dados para o formulário
    importFormData(data) {
        Object.keys(data).forEach(key => {
            const field = document.getElementById(key) || document.querySelector(`[name="${key}"]`);
            if (field) {
                if (field.type === 'checkbox') {
                    field.checked = data[key];
                } else {
                    field.value = data[key];
                }
            }
        });

        // Configurar permissões
        if (data.permissoes && Array.isArray(data.permissoes)) {
            data.permissoes.forEach(permission => {
                const checkbox = document.getElementById(`perm_${permission}`);
                if (checkbox) checkbox.checked = true;
            });
        }
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // Ler dados fornecidos pelo servidor via script[type="application/json"]
    const dataEl = document.getElementById('fornecedor-server-data');
    let serverData = {};
    try {
        serverData = JSON.parse(dataEl.textContent || '{}');
    } catch (e) {
        // parsing error - nada a fazer
        serverData = {};
    }

    // Função auxiliar para criar e mostrar um toast/alert
    function showToast(message, type = 'danger', timeout = 8000) {
        const el = document.createElement('div');
        el.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
        el.style.zIndex = '9999';
        el.style.minWidth = '300px';
        el.innerHTML = `\n                        <strong>${type === 'success' ? '<i class="bi bi-check-circle-fill"></i> Sucesso!' : '<i class="bi bi-exclamation-triangle-fill"></i> Erro'}</strong><br>\n                        ${message}\n                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`;
        document.body.appendChild(el);
        setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 150); }, timeout);
    }

    // Mostrar erro geral
    if (serverData.erro) {
        showToast(serverData.erro, 'danger', 8000);
    }

    // Mostrar lista de erros (se houver)
    if (Array.isArray(serverData.erros_list) && serverData.erros_list.length) {
        serverData.erros_list.forEach(msg => showToast(msg, 'danger', 8000));
    }

    // Mostrar sucesso
    if (serverData.sucesso) {
        showToast(serverData.sucesso, 'success', 5000);
    }

    // (Opcional) focar/abrir a seção do formulário que contém o primeiro erro de campo
    try {
        const campos = serverData.campos_erro || {};
        const camposKeys = Object.keys(campos);
        if (camposKeys.length) {
            // mapear campos para seções (ajuste conforme nomes de campos)
            const mapaSecao = {
                'nome': 1, 'razao_social': 1, 'cpf_cnpj': 1, 'telefone': 1,
                'estado': 2, 'cidade': 2, 'cep': 2, 'rua': 2, 'bairro': 2, 'numero': 2, 'complemento': 2,
                'email': 3, 'senha': 3, 'confirmar_senha': 3, 'termos': 3
            };
            const primeira = camposKeys[0];
            const secao = mapaSecao[primeira] || 1;
            // esconder todas as seções e mostrar a desejada
            document.querySelectorAll('.form-section').forEach(s => s.classList.add('d-none'));
            const el = document.getElementById(`secao${secao}`);
            if (el) el.classList.remove('d-none');
            // rolar até o formulário
            const formTop = document.querySelector('.cadastro-form-container');
            if (formTop) formTop.scrollIntoView({ behavior: 'smooth' });
        }
    } catch (e) {
        // silencioso
    }
});
