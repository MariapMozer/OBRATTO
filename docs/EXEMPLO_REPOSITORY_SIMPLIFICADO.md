# Exemplo: Simplificação do Repository Pattern

## 📋 Contexto

Atualmente, cada entidade do sistema possui 3 arquivos separados:
- `*_model.py` - Define a estrutura de dados (dataclass)
- `*_sql.py` - Contém as queries SQL como strings
- `*_repo.py` - Implementa as operações de banco de dados

**Total:** 16 entidades x 3 arquivos = **48 arquivos** apenas para acesso a dados!

## 🎯 Objetivo da Simplificação

Unificar esses 3 arquivos em **1 único arquivo** por entidade, reduzindo:
- De 48 arquivos para 16 arquivos
- Complexidade de navegação no código
- Dificuldade de manutenção
- Abstrações desnecessárias para nível acadêmico

---

## 📝 EXEMPLO: Entidade Usuario

### ❌ ANTES: 3 Arquivos Separados

#### Arquivo 1: `data/usuario/usuario_model.py` (56 linhas)
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha: str
    cpf_cnpj: str
    telefone: str
    cep: str
    rua: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    estado: str
    tipo_usuario: str
    data_cadastro: Optional[str] = None
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Usuario":
        return cls(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            # ... mais 15 campos
        )
```

#### Arquivo 2: `data/usuario/usuario_sql.py` (100+ linhas)
```python
CRIAR_TABELA_USUARIO = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        # ... mais campos
    );
"""

INSERIR_USUARIO = """
INSERT INTO usuario (...) VALUES (?, ?, ?, ...);
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT * FROM usuario WHERE email = ?;
"""

# ... mais 10 queries
```

#### Arquivo 3: `data/usuario/usuario_repo.py` (200+ linhas)
```python
from data.usuario.usuario_model import Usuario
from data.usuario.usuario_sql import *
from util.db import open_connection

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_USUARIO, (...))
        conn.commit()
        return cursor.lastrowid

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_USUARIO_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            return Usuario.from_row(row)
        return None

# ... mais 10 funções
```

**Total ANTES:** ~350 linhas em 3 arquivos

---

### ✅ DEPOIS: 1 Arquivo Unificado

#### Arquivo Único: `data/usuario.py` (~180 linhas)

```python
"""
Módulo Usuario - Gerenciamento de usuários do sistema

Este módulo unifica:
- Modelo de dados (classe Usuario)
- Queries SQL
- Operações de banco de dados

Simplificado para facilitar compreensão e manutenção.
"""

import sqlite3
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# HELPER: Conexão com Banco
# ============================================================================

def get_db():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect('obratto.db')
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================================
# CLASSE: Usuario
# ============================================================================

class Usuario:
    """
    Representa um usuário do sistema.

    Attributes:
        id: ID único do usuário
        nome: Nome completo
        email: Email (usado para login)
        senha: Senha hash (bcrypt)
        cpf_cnpj: CPF ou CNPJ
        telefone: Telefone de contato
        cep, rua, numero, complemento, bairro, cidade, estado: Endereço
        tipo_usuario: cliente, prestador, fornecedor ou administrador
        data_cadastro: Data de registro
        foto: URL da foto de perfil
        token_redefinicao: Token para reset de senha
        data_token: Data de expiração do token
    """

    def __init__(self, id=None, nome='', email='', senha='', cpf_cnpj='',
                 telefone='', cep='', rua='', numero='', complemento='',
                 bairro='', cidade='', estado='', tipo_usuario='cliente',
                 data_cadastro=None, foto=None, token_redefinicao=None,
                 data_token=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf_cnpj = cpf_cnpj
        self.telefone = telefone
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.tipo_usuario = tipo_usuario
        self.data_cadastro = data_cadastro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.foto = foto
        self.token_redefinicao = token_redefinicao
        self.data_token = data_token

    def __repr__(self):
        return f"Usuario(id={self.id}, email={self.email}, tipo={self.tipo_usuario})"

    def to_dict(self):
        """Converte o usuário para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf_cnpj': self.cpf_cnpj,
            'telefone': self.telefone,
            'cep': self.cep,
            'rua': self.rua,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'tipo_usuario': self.tipo_usuario,
            'data_cadastro': self.data_cadastro,
            'foto': self.foto
        }

    # ========================================================================
    # MÉTODOS DE CLASSE (equivalente ao Repository)
    # ========================================================================

    @staticmethod
    def criar_tabela():
        """Cria a tabela de usuários se não existir"""
        conn = get_db()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                cpf_cnpj TEXT NOT NULL,
                telefone TEXT NOT NULL,
                cep TEXT NOT NULL,
                rua TEXT NOT NULL,
                numero TEXT NOT NULL,
                complemento TEXT,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                data_cadastro TEXT NOT NULL,
                foto TEXT,
                token_redefinicao TEXT,
                data_token TIMESTAMP,
                tipo_usuario TEXT NOT NULL DEFAULT 'cliente'
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Tabela 'usuario' criada/verificada")

    def salvar(self):
        """
        Salva o usuário no banco (INSERT ou UPDATE).

        Returns:
            O próprio usuário com ID atualizado
        """
        conn = get_db()

        if self.id:
            # UPDATE
            conn.execute("""
                UPDATE usuario
                SET nome=?, email=?, senha=?, cpf_cnpj=?, telefone=?,
                    cep=?, rua=?, numero=?, complemento=?, bairro=?,
                    cidade=?, estado=?, foto=?, token_redefinicao=?,
                    data_token=?, tipo_usuario=?
                WHERE id=?
            """, (
                self.nome, self.email, self.senha, self.cpf_cnpj,
                self.telefone, self.cep, self.rua, self.numero,
                self.complemento, self.bairro, self.cidade, self.estado,
                self.foto, self.token_redefinicao, self.data_token,
                self.tipo_usuario, self.id
            ))
            logger.info(f"Usuário ID {self.id} atualizado")
        else:
            # INSERT
            cursor = conn.execute("""
                INSERT INTO usuario (
                    nome, email, senha, cpf_cnpj, telefone,
                    cep, rua, numero, complemento, bairro,
                    cidade, estado, data_cadastro, foto,
                    token_redefinicao, data_token, tipo_usuario
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.nome, self.email, self.senha, self.cpf_cnpj,
                self.telefone, self.cep, self.rua, self.numero,
                self.complemento, self.bairro, self.cidade, self.estado,
                self.data_cadastro, self.foto, self.token_redefinicao,
                self.data_token, self.tipo_usuario
            ))
            self.id = cursor.lastrowid
            logger.info(f"Novo usuário criado com ID {self.id}")

        conn.commit()
        conn.close()
        return self

    def deletar(self):
        """Remove o usuário do banco"""
        if not self.id:
            raise ValueError("Não é possível deletar usuário sem ID")

        conn = get_db()
        conn.execute("DELETE FROM usuario WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
        logger.info(f"Usuário ID {self.id} deletado")

    @staticmethod
    def buscar_por_id(usuario_id: int) -> Optional['Usuario']:
        """Busca usuário por ID"""
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM usuario WHERE id = ?", (usuario_id,)
        ).fetchone()
        conn.close()

        if row:
            return Usuario(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                senha=row['senha'],
                cpf_cnpj=row['cpf_cnpj'],
                telefone=row['telefone'],
                cep=row['cep'],
                rua=row['rua'],
                numero=row['numero'],
                complemento=row['complemento'],
                bairro=row['bairro'],
                cidade=row['cidade'],
                estado=row['estado'],
                tipo_usuario=row['tipo_usuario'],
                data_cadastro=row['data_cadastro'],
                foto=row['foto'],
                token_redefinicao=row['token_redefinicao'],
                data_token=row['data_token']
            )
        return None

    @staticmethod
    def buscar_por_email(email: str) -> Optional['Usuario']:
        """Busca usuário por email"""
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM usuario WHERE email = ?", (email,)
        ).fetchone()
        conn.close()

        if row:
            return Usuario(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                senha=row['senha'],
                cpf_cnpj=row['cpf_cnpj'],
                telefone=row['telefone'],
                cep=row['cep'],
                rua=row['rua'],
                numero=row['numero'],
                complemento=row['complemento'],
                bairro=row['bairro'],
                cidade=row['cidade'],
                estado=row['estado'],
                tipo_usuario=row['tipo_usuario'],
                data_cadastro=row['data_cadastro'],
                foto=row['foto'],
                token_redefinicao=row['token_redefinicao'],
                data_token=row['data_token']
            )
        return None

    @staticmethod
    def listar_todos() -> List['Usuario']:
        """Lista todos os usuários"""
        conn = get_db()
        rows = conn.execute("SELECT * FROM usuario ORDER BY id").fetchall()
        conn.close()

        usuarios = []
        for row in rows:
            usuarios.append(Usuario(
                id=row['id'],
                nome=row['nome'],
                email=row['email'],
                senha=row['senha'],
                cpf_cnpj=row['cpf_cnpj'],
                telefone=row['telefone'],
                cep=row['cep'],
                rua=row['rua'],
                numero=row['numero'],
                complemento=row['complemento'],
                bairro=row['bairro'],
                cidade=row['cidade'],
                estado=row['estado'],
                tipo_usuario=row['tipo_usuario'],
                data_cadastro=row['data_cadastro'],
                foto=row['foto'],
                token_redefinicao=row['token_redefinicao'],
                data_token=row['data_token']
            ))
        return usuarios

    @staticmethod
    def listar_por_tipo(tipo_usuario: str) -> List['Usuario']:
        """Lista usuários de um tipo específico"""
        conn = get_db()
        rows = conn.execute(
            "SELECT * FROM usuario WHERE tipo_usuario = ? ORDER BY id",
            (tipo_usuario,)
        ).fetchall()
        conn.close()

        return [Usuario(**dict(row)) for row in rows]


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Criar tabela
    Usuario.criar_tabela()

    # Criar novo usuário
    novo_usuario = Usuario(
        nome="João Silva",
        email="joao@example.com",
        senha="hash_da_senha",
        cpf_cnpj="12345678900",
        telefone="2799999999",
        cep="29000-000",
        rua="Rua Exemplo",
        numero="123",
        complemento="Apto 101",
        bairro="Centro",
        cidade="Vitória",
        estado="ES",
        tipo_usuario="cliente"
    )
    novo_usuario.salvar()
    print(f"Usuário criado: {novo_usuario}")

    # Buscar por email
    usuario = Usuario.buscar_por_email("joao@example.com")
    if usuario:
        print(f"Usuário encontrado: {usuario}")

    # Atualizar
    usuario.telefone = "2788888888"
    usuario.salvar()

    # Listar todos
    todos = Usuario.listar_todos()
    print(f"Total de usuários: {len(todos)}")

    # Deletar
    # usuario.deletar()
```

**Total DEPOIS:** ~180 linhas em 1 arquivo

---

## 📊 Comparação

| Aspecto | ANTES (Repository Pattern) | DEPOIS (Simplificado) |
|---------|---------------------------|----------------------|
| **Arquivos** | 3 arquivos | 1 arquivo |
| **Linhas de código** | ~350 linhas | ~180 linhas |
| **Complexidade** | Alta (abstrações) | Baixa (direto) |
| **Navegação** | Saltar entre 3 arquivos | Tudo em um lugar |
| **Compreensão** | Requer entender padrões | Código auto-explicativo |
| **Manutenção** | 3 arquivos para atualizar | 1 arquivo para atualizar |
| **Imports** | `from data.usuario.usuario_repo import *` | `from data.usuario import Usuario` |

---

## 🔄 Como Usar no Código

### Antes (Repository Pattern):
```python
# Nas rotas
from data.usuario.usuario_repo import inserir_usuario, obter_usuario_por_email
from data.usuario.usuario_model import Usuario

# Criar usuário
novo = Usuario(nome="João", email="joao@test.com", ...)
id_usuario = inserir_usuario(novo)

# Buscar
usuario = obter_usuario_por_email("joao@test.com")
```

### Depois (Simplificado):
```python
# Nas rotas
from data.usuario import Usuario

# Criar usuário
novo = Usuario(nome="João", email="joao@test.com", ...)
novo.salvar()

# Buscar
usuario = Usuario.buscar_por_email("joao@test.com")
```

**Mais simples e orientado a objetos!**

---

## 🛠️ Passos para Aplicar em Outras Entidades

### 1. Escolha uma entidade (ex: `cliente`)

### 2. Crie o novo arquivo unificado
```bash
# Criar novo arquivo
touch data/cliente_simplificado.py
```

### 3. Estrutura do arquivo:
```python
# 1. Imports
import sqlite3
from typing import Optional, List
from datetime import datetime

# 2. Helper de conexão
def get_db():
    conn = sqlite3.connect('obratto.db')
    conn.row_factory = sqlite3.Row
    return conn

# 3. Classe com atributos
class Cliente:
    def __init__(self, id=None, ...):
        self.id = id
        # ... outros atributos

    # 4. Métodos estáticos (equivalente ao repository)
    @staticmethod
    def criar_tabela():
        # SQL inline aqui

    def salvar(self):
        # INSERT ou UPDATE

    @staticmethod
    def buscar_por_id(id):
        # SELECT com WHERE

    @staticmethod
    def listar_todos():
        # SELECT *

    # ... outros métodos conforme necessário
```

### 4. Teste o novo arquivo
```python
# No terminal
python data/cliente_simplificado.py
```

### 5. Atualizar imports nas rotas
```python
# De:
from data.cliente.cliente_repo import inserir_cliente

# Para:
from data.cliente_simplificado import Cliente
```

### 6. Substituir chamadas
```python
# De:
id = inserir_cliente(cliente)

# Para:
cliente.salvar()
```

### 7. Deletar arquivos antigos (APÓS TESTAR!)
```bash
rm -rf data/cliente/
```

---

## ⚠️ IMPORTANTE - Recomendações

### NÃO é necessário simplificar AGORA
Esta simplificação é **opcional** e pode ser feita:
- Durante as férias/recesso
- Como refatoração futura
- Entidade por entidade gradualmente
- **OU simplesmente NUNCA** (o código atual funciona!)

### Se decidir simplificar:
1. ✅ Faça UMA entidade por vez
2. ✅ Teste completamente antes de prosseguir
3. ✅ Use Git para fazer backup antes
4. ✅ Crie um branch separado: `git checkout -b simplify-repository`
5. ✅ Peça ajuda se travar

### Priorize:
- ✅ Entender bem o código atual
- ✅ Fazer o projeto funcionar perfeitamente
- ✅ Preparar apresentação
- ❌ Refatorações arriscadas próximo à entrega

---

## 📚 Resumo

O **Repository Pattern** é um padrão de arquitetura excelente para projetos empresariais grandes, mas para um projeto acadêmico de ensino médio, a **versão simplificada** oferece:

- ✅ **Mesma funcionalidade**
- ✅ **50% menos código**
- ✅ **Muito mais fácil de entender**
- ✅ **Mais fácil de manter**
- ✅ **Orientação a objetos mais clara**

**Decisão:** Vocês escolhem! Ambas abordagens são válidas. O importante é que entendam o que estão fazendo.

---

**Documento criado em:** Outubro 2025
**Para:** Alunos do projeto OBRATTO
**Objetivo:** Demonstrar simplificação opcional do Repository Pattern
