from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Produto, Vender, Comprar, Fornecedor, Cliente, Usuario
from security import argon2_content
from dependencies import pegar_sessao, verificar_token
from schemas import VenderSchema, ComprarSchema


from sqlalchemy import func

order_router = APIRouter(prefix='/order', tags=['order'], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def home():
    return{
        "mensagem": "Área de compras e vendas",
        "teste4" : "foi"
    }

@order_router.post('/comprar_produtos')
async def comprar_produtos(comprar_schema:ComprarSchema, session: Session= Depends(pegar_sessao), usuario: Usuario=Depends(verificar_token)):
    comprar = session.query(Produto).filter(Produto.id == comprar_schema.produto_id).first()
    fornecedor = session.query(Fornecedor).filter(Fornecedor.id == comprar_schema.fornecedor_id).first()

    if not comprar or not fornecedor:
        raise HTTPException(status_code=404, detail="Não temos o produto cadastrado ou esse fornecedor em nossa base, tente primeiro adicionar")
    
    nova_compra= Comprar(comprar_schema.produto_id, comprar_schema.fornecedor_id, usuario.id, comprar_schema.preco_unitario, comprar_schema.quantidade)
    nova_compra.calcular_valor_total()

    comprar.entrada_estoque(comprar_schema.quantidade) 

    session.add(nova_compra)
    session.commit()

    return{
        "mensagem": "Produto comprado com sucesso! "
    }


@order_router.post('/vender_produtos')
async def vender_produtos(vender_schema:VenderSchema, session: Session= Depends(pegar_sessao),usuario: Usuario=Depends(verificar_token)):
    vender = session.query(Produto).filter(Produto.id == vender_schema.produto_id).first()
    cliente = session.query(Cliente).filter(Cliente.id == vender_schema.cliente_id).first()

    if not vender or not cliente:
        raise HTTPException(status_code=404, detail="Não temos o produto cadastrado ou esse cliente não está em nossa base, tente primeiro adicionar")
    
    nova_venda= Vender(vender_schema.produto_id, vender_schema.cliente_id, usuario.id, vender_schema.preco_unitario, vender_schema.quantidade)
    nova_venda.calcular_valor_total()

    vender.entrada_estoque(vender_schema.quantidade) 

    session.add(nova_venda)
    session.commit()

    return{
        "mensagem": "Produto vendido com sucesso! "
    }












    



    
