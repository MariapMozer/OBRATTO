# Scripts Utilitários do OBRATTO

Esta pasta contém scripts utilitários para manutenção e administração do sistema.

## 📁 Arquivos

### 🗄️ **Banco de Dados**
- **`atualizar_bd.py`** - Script de migração que adiciona colunas de endereço na tabela `usuario`
  - Adiciona: estado, cidade, rua, numero, bairro
  - Seguro para executar múltiplas vezes
  - **Uso:** `python scripts/atualizar_bd.py`

- **`criar_admin_padrao.py`** - Cria um administrador padrão no sistema
  - Email: admin@sistema.com
  - Senha: admin123
  - **Uso:** `python scripts/criar_admin_padrao.py`

### 🖼️ **Gerenciamento de Imagens**
- **`gerenciar_orfaos.py`** - Gerencia arquivos órfãos na pasta de uploads
  - **Modo interativo:** `python scripts/gerenciar_orfaos.py`
  - **Verificar:** `python scripts/gerenciar_orfaos.py verificar`
  - **Limpar:** `python scripts/gerenciar_orfaos.py limpar`
  - **Limpar sem confirmação:** `python scripts/gerenciar_orfaos.py limpar --force`
  - Lista arquivos no banco vs pasta, identifica órfãos e permite limpeza

## 🚀 Como usar

Execute os scripts sempre da raiz do projeto:

```bash
# Verificar arquivos órfãos
python scripts/verificar_orfaos.py

# Limpar arquivos órfãos
python scripts/limpar_orfaos.py

# Atualizar estrutura do banco
python scripts/atualizar_bd.py
```

## ⚠️ Avisos

- **Sempre faça backup** do banco de dados antes de executar scripts de migração
- **Teste em ambiente de desenvolvimento** antes de usar em produção
- Os scripts de limpeza **removem arquivos permanentemente**

## 📋 Manutenção Recomendada

- Execute `verificar_orfaos.py` **semanalmente** para monitorar o uso de disco
- Execute `limpar_orfaos.py` **quando necessário** para liberar espaço
- Mantenha backups regulares antes de executar qualquer script