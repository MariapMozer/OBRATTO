import pytest
from pydantic import ValidationError
from dtos.usuario_dto import CriarUsuarioDTO


def test_criar_usuario_valido():
    data = CriarUsuarioDTO.criar_exemplo_usuario_json()
    dto = CriarUsuarioDTO(**data)
    assert dto.nome == data['nome']
    assert dto.email == data['email']


def test_criar_usuario_senha_curta():
    data = CriarUsuarioDTO.criar_exemplo_usuario_json()
    data['senha'] = 'short1'
    data['confirmar_senha'] = 'short1'
    with pytest.raises(ValidationError) as excinfo:
        CriarUsuarioDTO(**data)
    errors = excinfo.value.errors()
    # esperar erro no campo 'senha'
    assert any(e['loc'] and e['loc'][0] == 'senha' for e in errors)


def test_criar_usuario_cpf_invalido():
    data = CriarUsuarioDTO.criar_exemplo_usuario_json()
    data['cpf_cnpj'] = '123'
    data['confirmar_senha'] = data['senha']
    with pytest.raises(ValidationError) as excinfo:
        CriarUsuarioDTO(**data)
    errors = excinfo.value.errors()
    # esperar erro relacionado ao campo cpf_cnpj
    assert any(e['loc'] and e['loc'][0] in ('cpf_cnpj',) for e in errors)
