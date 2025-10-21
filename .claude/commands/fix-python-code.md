# Fix Python Type Errors

Execute type checking com mypy e corrija automaticamente todos os erros de tipagem encontrados no código Python.

## Instruções

1. **Execute mypy para identificar problemas de tipagem**
   - Use: `mypy . --check-untyped-defs --show-column-numbers`
   - Conte o número total de erros
   - Analise os padrões de erros encontrados

2. **Identifique os padrões de erros comuns**:
   - Argumentos `int | None` sendo passados para parâmetros `int`
   - Acessar atributos de objetos que podem ser `None` sem verificação prévia
   - Tipos incorretos (ex: `str` para `date`, `str` para Enum)
   - Parâmetros incorretos em construtores

3. **Aplique as correções seguindo estes padrões**:

### Padrão 1: Asserts após funções de inserção
Quando funções como `inserir_usuario()`, `inserir_tutor()`, `inserir_veterinario()`, `inserir()`, `inserir_chamado()`, etc. retornam `Optional[int]`:

```python
# ANTES:
id_usuario = inserir_usuario(usuario_teste)
chamado = Chamado(id_usuario=id_usuario, ...)  # Erro: int | None não pode ser int

# DEPOIS:
id_usuario = inserir_usuario(usuario_teste)
assert id_usuario is not None
chamado = Chamado(id_usuario=id_usuario, ...)  # OK
```

### Padrão 2: Asserts antes de acessar atributos
Quando objetos retornados podem ser `None`:

```python
# ANTES:
usuario = obter_por_id(id)
assert usuario.nome == "João"  # Erro: None não tem atributo 'nome'

# DEPOIS:
usuario = obter_por_id(id)
assert usuario is not None
assert usuario.nome == "João"  # OK
```

### Padrão 3: Corrigir tipos incorretos
Para strings que deveriam ser dates, datetimes ou Enums:

```python
# ANTES:
from datetime import date
chamado = Chamado(
    status="aberto",  # Erro: str não pode ser ChamadoStatus
    data="2025-06-30"  # Erro: str não pode ser datetime
)

# DEPOIS:
from datetime import datetime
from model.enums import ChamadoStatus

chamado = Chamado(
    status=ChamadoStatus.ABERTO,  # OK
    data=datetime(2025, 6, 30)  # OK
)
```

### Padrão 4: Corrigir parâmetros de construtores
Verifique os nomes corretos dos parâmetros nos modelos:

```python
# ANTES:
admin = Administrador(id=0, ...)  # Erro: parâmetro desconhecido

# DEPOIS:
admin = Administrador(id_admin=0, ...)  # OK
```

### Padrão 5: Atualizar modelos quando necessário
Se muitos testes precisam de `None` em um campo, considere atualizar o modelo:

```python
# ANTES (model/denuncia_model.py):
@dataclass
class Denuncia:
    id_denuncia: Optional[int]
    id_usuario: int
    id_admin: int  # Não permite None

# DEPOIS:
from typing import Optional

@dataclass
class Denuncia:
    id_denuncia: Optional[int]
    id_usuario: int
    id_admin: Optional[int]  # Agora permite None
```

4. **Priorize a correção por arquivo**:
   - Comece pelos arquivos com mais erros
   - Agrupe correções similares para eficiência
   - Use `replace_all=true` quando aplicável

5. **Remova type ignores desnecessários**:
   ```python
   # ANTES:
   resultado = funcao(id_var)  # type: ignore[arg-type]

   # DEPOIS (após adicionar assert):
   assert id_var is not None
   resultado = funcao(id_var)  # Não precisa mais de ignore
   ```

6. **Verifique imports necessários**:
   - `from datetime import date, datetime`
   - `from typing import Optional`
   - `from model.enums import ChamadoStatus, DenunciaStatus, VerificacaoStatus`

7. **Verificação final**:
   - Execute: `mypy . --check-untyped-defs --show-column-numbers`
   - Confirme que não há mais erros
   - Reporte o número de arquivos verificados e o status final

## Exemplo de Relatório Final

Ao concluir, forneça um resumo como:

```
✅ Todos os erros de tipagem foram corrigidos!

Resultados:
- Erros iniciais: 261
- Erros finais: 0
- Taxa de sucesso: 100%

Arquivos verificados: 201
Status: Success: no issues found

Principais correções:
- Adicionados asserts após funções de inserção
- Adicionados asserts antes de acessar atributos
- Corrigidos tipos incorretos (str → date/datetime/Enum)
- Atualizados modelos para aceitar Optional quando necessário
```

## Notas Importantes

- **NÃO refatore o código** - apenas corrija erros de tipagem
- **NÃO adicione funcionalidades** - mantenha a lógica existente
- **NÃO remova testes** - apenas corrija para passar no mypy
- **SEMPRE verifique** se há imports necessários antes de usar tipos
- **USE replace_all=true** quando o mesmo padrão se repete múltiplas vezes
- **SEMPRE execute mypy** no final para confirmar que todos os erros foram corrigidos
