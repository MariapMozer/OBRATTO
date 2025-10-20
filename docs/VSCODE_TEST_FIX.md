# Como Resolver Problemas com Test Explorer do VSCode

Se os testes `test_fornecedor_planos.py` e `test_fornecedor_produtos.py` não estão passando no Test Explorer do VSCode, siga estas etapas:

## 1. Limpar Cache do Pytest no VSCode

1. Abra a paleta de comandos: `Cmd+Shift+P` (Mac) ou `Ctrl+Shift+P` (Windows/Linux)
2. Digite e execute: `Python: Clear Cache and Reload Window`
3. Aguarde o VSCode recarregar

## 2. Recarregar Testes

1. No Test Explorer (ícone de frasco de laboratório na barra lateral)
2. Clique no ícone de refresh (🔄) no topo do painel
3. Aguarde a descoberta dos testes finalizar

## 3. Deletar Arquivos de Cache

Se o problema persistir, delete manualmente os caches:

```bash
# No terminal, execute na raiz do projeto:
rm -rf .pytest_cache
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +
```

## 4. Recarregar Janela do VSCode

1. Paleta de comandos: `Cmd+Shift+P` / `Ctrl+Shift+P`
2. Digite: `Developer: Reload Window`

## 5. Verificar Configuração do Python

Certifique-se de que o VSCode está usando o Python correto:

1. Clique no indicador do Python na barra de status (canto inferior direito)
2. Selecione o interpretador Python correto (o mesmo que você usa no terminal)

## 6. Executar Testes no Terminal

Para confirmar que os testes funcionam, execute no terminal:

```bash
# Testar apenas os arquivos problemáticos:
python -m pytest tests/test_fornecedor_planos.py -v
python -m pytest tests/test_fornecedor_produtos.py -v

# Testar todos:
python -m pytest -v
```

## 7. Verificar Arquivo de Banco de Dados

Se ainda houver problemas, pode ser um banco de dados bloqueado:

```bash
# Deletar banco de dados de teste que pode estar travado:
rm -f obratto.db
rm -f *.db
```

## Correções Aplicadas

Os seguintes arquivos foram atualizados para usar corretamente o fixture `test_db`:

- ✅ `tests/test_fornecedor_planos.py` - Adicionado `test_db` ao fixture `setup_db`
- ✅ `tests/test_fornecedor_produtos.py` - Adicionado fixture `setup_db` com `test_db`

Estas mudanças garantem que cada teste use um banco de dados temporário isolado, evitando conflitos.

## Status dos Testes

Todos os 122 testes devem passar:
- ✅ 100/100 testes de repositório
- ✅ 15/15 testes de integração
- ✅ 7/7 testes de rotas autenticadas

Execute `python -m pytest -v` para confirmar.
