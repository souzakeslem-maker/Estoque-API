from fastapi import FastAPI

from auth_routes import auth_router
from order_routes import order_router
from analysis_routes import analysis_router
from register_routes import register_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(analysis_router)
app.include_router(register_router)

@app.get('/')
async def home():
    return{
        "mensagem": "Bem-vindo ao sistema de estoque!"
    }



