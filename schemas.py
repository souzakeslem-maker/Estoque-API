from pydantic import BaseModel
from typing import List, Optional

class ClienteSchema(BaseModel):
    nome: str
    cnpj: int
    telefone: int

    class Config:
        from_attributes = True

class FornecedorSchema(BaseModel):
    nome: str
    cnpj: int
    telefone: int

    class Config:
        from_attributes = True

class ProdutoSchema(BaseModel):
    usuario_id: int
    nome : str
    estoque : int
    preco : float

    class Config:
        from_attributes = True

class ComprarSchema(BaseModel):
    produto_id : int
    fornecedor_id : int
    preco_unitario : float
    quantidade: int

    class Config:
        from_attributes = True

class VenderSchema(BaseModel):
    produto_id : int
    cliente_id : int
    preco_unitario : float
    quantidade: int

    class Config:
        from_attributes = True

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    telefone: int
    admin: bool
    senha: str

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True




