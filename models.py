from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, ForeignKey, String, Integer, Boolean, Float, Column

db = create_engine('sqlite:///banco.db')
base = declarative_base()

class Cliente(base):
    __tablename__ = "cliente"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    cnpj = Column("cnpj", Integer)
    telefone = Column("telefone", Integer)

    def __init__(self, nome, cnpj, telefone):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone

class Fornecedor(base):
    __tablename__ = "fornecedor"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String )
    cnpj = Column("cnpj", Integer)
    telefone = Column("telefone", Integer)

    def __init__(self, nome, cnpj, telefone):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone

class Produto(base):
    __tablename__ = "produtos"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    usuario_id = Column('usuario_id', Integer, ForeignKey('usuario.id'))
    nome = Column("nome", String)
    estoque = Column("estoque", Integer, default=0)
    preco = Column("preco", Float)

    def __init__(self, usuario_id, nome, estoque, preco):
        self.usuario_id = usuario_id
        self.nome = nome
        self.estoque = estoque 
        self.preco = preco

    def entrada_estoque(self, quantidade):
        self.estoque += quantidade

    def saida_estoque(self, quantidade):
        if quantidade > self.estoque:
            raise ValueError('Estoque insuficiente')
        self.estoque -= quantidade 

class Comprar(base):
    __tablename__ = "comprar"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    produto_id = Column("produto_id",Integer, ForeignKey("produtos.id"))
    fornecedor_id = Column("fornecedor_id",Integer, ForeignKey('fornecedor.id') )
    usuario_id = Column('usuario_id', Integer, ForeignKey('usuario.id'))
    preco_unitario = Column("preco unitario", Float)
    quantidade = Column("quantidade", Integer)
    valor_total = Column('valor total', Float)
    produto = relationship('Produto', cascade="all, delete")
    
    

    def __init__(self,produto_id, fornecedor_id, usuario_id, preco_unitario, quantidade, valor_total=0):
        self.produto_id = produto_id
        self.fornecedor_id = fornecedor_id
        self.usuario_id = usuario_id
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade
        self.valor_total = valor_total

    def calcular_valor_total(self):
        self.valor_total = self.quantidade * self.preco_unitario



class Vender(base):
    __tablename__ = "vender"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    produto_id = Column("produto_id",Integer, ForeignKey("produtos.id"))
    cliente_id = Column("cliente_id",Integer, ForeignKey('cliente.id') )
    usuario_id = Column('usuario_id', Integer, ForeignKey('usuario.id'))
    preco_unitario = Column("preco unitario", Float)
    quantidade = Column("quantidade", Integer)
    valor_total = Column('valor total', Float)
    produto = relationship('Produto', cascade="all, delete")
    

    def __init__(self,produto_id, cliente_id, usuario_id, preco_unitario, quantidade, valor_total=0):
        self.produto_id = produto_id
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade
        self.valor_total = valor_total

    def calcular_valor_total(self):
        self.valor_total = self.quantidade * self.preco_unitario


class Usuario(base):
    __tablename__ = 'usuario'
    id = Column("id",Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String )
    email = Column("email", Integer)
    telefone = Column("telefone", Integer)
    admin = Column('admin', Boolean)
    senha = Column('senha', String)

    def __init__(self, nome, email, telefone, admin, senha):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.admin = admin
        self.senha = senha










