from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Produto, Vender, Comprar, Fornecedor, Cliente, Usuario
from security import argon2_content
from dependencies import pegar_sessao, verificar_token
from schemas import ProdutoSchema, VenderSchema, ComprarSchema


from sqlalchemy import func

analysis_router = APIRouter(prefix='/analysis', tags=['analysis'], dependencies=[Depends(verificar_token)])

def verificar_admin(
    usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem acessar esta rota"
        )

    return usuario

@analysis_router.get("/")
async def home():
    return{
        "mensagem": "Área de análise de vendas"
    }

@analysis_router.get('/relatorio_compras')
async def listar_pedidos(session: Session = Depends(pegar_sessao)):
    compras = session.query(Comprar).all()
    return{
        "Compras" : compras
    }

@analysis_router.get('/Relatorio_vendas')
async def listar_vendas(session: Session = Depends(pegar_sessao)):
    vendas = session.query(Vender).all()
    return{
        "Vendas" : vendas
    }



@analysis_router.get('/quantidade_vendas')
async def listar_vendas(session: Session = Depends(pegar_sessao)):

    total = session.query(func.sum(Vender.quantidade)).scalar()

    return {
        "quantidade_vendida": total or 0
    }


@analysis_router.get('/quantidade_compras')
async def somar_compras(session: Session = Depends(pegar_sessao)):

    total = session.query(func.sum(Comprar.quantidade)).scalar()

    return {
        "quantidade_comprada": total or 0
    }


@analysis_router.get('/somar_compras')
async def somar_compras(session: Session = Depends(pegar_sessao)):

    total = session.query(func.sum(Comprar.valor_total)).scalar()

    return {
        "valor_gasto": total or 0
    }


@analysis_router.get('/somar_vendas')
async def somar_vendas(session: Session = Depends(pegar_sessao)):

    total = session.query(func.sum(Vender.valor_total)).scalar()

    return {
        "valor_arrecadado": total or 0
    }

@analysis_router.get('/caixa_atual')
async def somar_vendas(session: Session = Depends(pegar_sessao), usuario_logado: Usuario = Depends(verificar_admin)):
    if not usuario_logado.admin:
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem cadastrar colaboradores"
        )
    vender = session.query(func.sum(Vender.valor_total)).scalar()

    comprar = session.query(func.sum(Comprar.valor_total)).scalar()
    total = vender - comprar
    
    return {
        "valor_arrecadado": f"{int(total)or 0},00"
    }


@analysis_router.get('/listar_vendas_cliente/{cliente_id}')
async def listar_vendas_cliente(cliente_id: int,session: Session = Depends(pegar_sessao)):
    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).scalar()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado, tente primeiro adicionar")


    quantidade = session.query(func.sum(Vender.quantidade)).filter(Vender.cliente_id == cliente_id).scalar()
    gasto_total = session.query(func.sum(Vender.valor_total)).filter(Vender.cliente_id ==  cliente_id).scalar()
    if gasto_total != None:
        return{
            "cliente_id": cliente_id,
            "quantidade_comprada": quantidade or 0,
            "Gasto_total" : f"R${int(gasto_total) or 0},00"
        }


    return{
        "cliente_id": cliente_id,
        "quantidade_comprada": quantidade or 0,
        "Gasto_total" : f"R${gasto_total or 0},00" 
    }

@analysis_router.get('/listar_compras_fornecededor/{fornecedor_id}')
async def listar_compras_fornecedores(fornecedor_id: int,session: Session = Depends(pegar_sessao)):
    fornecedor = session.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).scalar()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="fornecedor não encontrado, tente primeiro adicionar")
    
    
    quantidade = session.query(func.sum(Comprar.quantidade)).filter(Comprar.fornecedor_id == fornecedor_id).scalar()
    gasto_total = session.query(func.sum(Comprar.valor_total)).filter(Comprar.fornecedor_id ==  fornecedor_id).scalar()

    return{
        "fornecedor_id": fornecedor_id,
        "quantidade_comprada": quantidade or 0,
        "Gasto_total" : f"R${int(gasto_total) or 0},00" 

    }