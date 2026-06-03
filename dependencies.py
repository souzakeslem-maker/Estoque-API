from sqlalchemy.orm import Session, sessionmaker
from models import db, Usuario
from security import ALGORITHM, SECRET_KEY, oauth2
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


'''def verificar_token(token: str= Depends(oauth2), session: Session=Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get('sub'))

    except:
        usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
        if not usuario:
            raise HTTPException(status_code = 401, detail="Erro")
        return usuario
        '''

def verificar_token(token: str = Depends(oauth2),session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        id_usuario = int(dic_info.get('sub'))

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    usuario = session.query(Usuario).filter(
        Usuario.id == id_usuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return usuario




