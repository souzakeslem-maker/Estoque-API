from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Cliente, Fornecedor, Produto
from security import argon2_content
from dependencies import pegar_sessao, verificar_token
from schemas import ClienteSchema, FornecedorSchema, ProdutoSchema


register_router = APIRouter(prefix="/register", tags=['register'], dependencies=[Depends(verificar_token)])

@register_router.get("/")
async def home():
    return{
        "mensagem": "Área de adição de fornecedores e clientes"
    }

@register_router.post('/criar_fornecedor')
async def criar_fornecedor(fornecedor_schema: FornecedorSchema, session: Session= Depends(pegar_sessao)):
    '''
    tentativa 03
    '''
    nome = session.query(Fornecedor).filter(fornecedor_schema.nome == Fornecedor.nome).first()
    if nome:
        raise HTTPException(status_code=401, detail="Fornecedor já está cadastrado em nossa base")
    else:
        novo_fornecedor = Fornecedor(fornecedor_schema.nome, fornecedor_schema.cnpj, fornecedor_schema.telefone)
        session.add(novo_fornecedor)
        session.commit()
        return{
            "mensagem" : "Fornecedor cadastrado com sucesso!"
        }

@register_router.post('/cadastrar_cliente')
async def cadastrar_cliente(cliente_schema: ClienteSchema, session: Session= Depends(pegar_sessao)):
    '''
    tentativa 00
    '''
    nome = session.query(Cliente).filter(cliente_schema.nome == Cliente.nome).first()
    if nome:
        raise HTTPException(status_code=401, detail="Cliente já está cadastrado em nossa base")
    else:
        novo_cliente = Cliente(cliente_schema.nome, cliente_schema.cnpj, cliente_schema.telefone)
        session.add(novo_cliente)
        session.commit()
        return{
            "mensagem" : "Cliente cadastrado com sucesso!"
        }


@register_router.post('/cadastrar_produto')
async def cadastrar_produto(produto_schema: ProdutoSchema, session: Session= Depends(pegar_sessao)):
    '''
    tentativa 00
    '''
    nome = session.query(Produto).filter(produto_schema.nome == Produto.nome).first()

    if nome:
        raise HTTPException(status_code=401, detail="Produto já está cadastrado em nossa base")
    else:
        novo_produto = Produto(produto_schema.usuario_id ,produto_schema.nome, produto_schema.estoque, produto_schema.preco)
        session.add(novo_produto)
        session.commit()
        return{
            "mensagem" : "Produto cadastrado com sucesso!"
        }