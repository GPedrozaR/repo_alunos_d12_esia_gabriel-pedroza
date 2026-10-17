"""Cadastro de clientes."""

import re

_CLIENTES = []
_EMAIL = re.compile(r"^[^@\s]+@[^@\s.]+\.[^@\s]+$")


def _cpf_valido(cpf):
    digitos = re.sub(r"\D", "", cpf)
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    for tamanho in (9, 10):
        soma = sum(int(d) * peso for d, peso in zip(digitos[:tamanho], range(tamanho + 1, 1, -1)))
        if int(digitos[tamanho]) != (soma * 10 % 11) % 10:
            return False
    return True


def cadastrar_cliente(payload):
    """Cadastra um cliente; cadastro inválido devolve 422 com todos os erros."""
    erros = []
    if not payload.get("nome"):
        erros.append({"campo": "nome", "erro": "obrigatório"})
    email = payload.get("email")
    if not email:
        erros.append({"campo": "email", "erro": "obrigatório"})
    elif not _EMAIL.match(email):
        erros.append({"campo": "email", "erro": "formato inválido"})
    cpf = payload.get("cpf")
    if not cpf:
        erros.append({"campo": "cpf", "erro": "obrigatório"})
    elif not _cpf_valido(str(cpf)):
        erros.append({"campo": "cpf", "erro": "inválido"})
    if erros:
        return 422, {"erros": erros}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
