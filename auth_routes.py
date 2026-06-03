from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from models import Usuario
from security import argon2_content, oauth2, TOKEN_ACCESS_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from dependencies import pegar_sessao, verificar_token
from schemas import UsuarioSchema, LoginSchema


auth_router = APIRouter(prefix="/auth", tags=['auth'])

def criar_token(id_usuario, duracao = timedelta(minutes= TOKEN_ACCESS_EXPIRE_MINUTES)):
    data_exp = datetime.now(timezone.utc) + timedelta(minutes= TOKEN_ACCESS_EXPIRE_MINUTES)
    dic_info = {'sub': str(id_usuario), 'exp': data_exp}
    jwt_codificador = jwt.encode(dic_info, SECRET_KEY, ALGORITHM) 
    return jwt_codificador

def autenticar(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not argon2_content.verify(senha, usuario.senha):
        return False
    return usuario

def verificar_admin(
    usuario: Usuario = Depends(verificar_token)
):
    if not usuario.admin:
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem acessar esta rota"
        )

    return usuario



@auth_router.get("/")
async def home():
    return{
        "mensagem": "Área de login"
    }

@auth_router.post('/cadastro')
async def cadastro(usuario_schema: UsuarioSchema, session: Session=Depends(pegar_sessao), usuario_logado: Usuario = Depends(verificar_admin)):
    '''
    teste 10
    '''
    if not usuario_logado.admin:
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem cadastrar colaboradores"
        )
    
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=409, detail='Usuario já cadastrado, tente novamente')

    else:
        senha_criptografada = argon2_content.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, usuario_schema.telefone, usuario_schema.admin, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return{
            "mensagem": "Usuário cadastrado com sucesso! "
        }
    

@auth_router.post('/login-form')
async def login_form(data_form: OAuth2PasswordRequestForm= Depends(), session: Session=Depends(pegar_sessao)):
    usuario = autenticar(data_form.username, data_form.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return{
            "access_token" : access_token,
            "token_type" : "Bearer"
        } 

 




