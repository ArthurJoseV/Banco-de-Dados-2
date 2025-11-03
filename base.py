from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

livro_autor = Table('livro_autor', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('livro_id', Integer, ForeignKey('livros.id')),
    Column('autor_id', Integer, ForeignKey('autores.id')),
    Column('data_associacao', DateTime, default=datetime.now)
)

livro_categoria = Table('livro_categoria', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('livro_id', Integer, ForeignKey('livros.id')),
    Column('categoria_id', Integer, ForeignKey('categorias.id')),
    Column('data_associacao', DateTime, default=datetime.now)
)

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(20))
    endereco = Column(Text)
    data_cadastro = Column(DateTime, default=datetime.now)
    ativo = Column(Boolean, default=True)
    
    emprestimos = relationship("Emprestimo", back_populates="usuario")
    reservas = relationship("Reserva", back_populates="usuario")
    multas = relationship("Multa", back_populates="usuario")

class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    isbn = Column(String(20), unique=True)
    ano_publicacao = Column(Integer)
    editora = Column(String(100))
    quantidade_total = Column(Integer, default=1)
    quantidade_disponivel = Column(Integer, default=1)
    data_cadastro = Column(DateTime, default=datetime.now)
    
    autores = relationship("Autor", secondary=livro_autor, back_populates="livros")
    categorias = relationship("Categoria", secondary=livro_categoria, back_populates="livros")
    emprestimos = relationship("Emprestimo", back_populates="livro")
    reservas = relationship("Reserva", back_populates="livro")

class Autor(Base):
    __tablename__ = 'autores'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    nacionalidade = Column(String(50))
    data_nascimento = Column(Date)
    data_falecimento = Column(Date, nullable=True)
    biografia = Column(Text)
    
    livros = relationship("Livro", secondary=livro_autor, back_populates="autores")

class Categoria(Base):
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False, unique=True)
    descricao = Column(Text)
    data_criacao = Column(DateTime, default=datetime.now)
    
    livros = relationship("Livro", secondary=livro_categoria, back_populates="categorias")

class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    livro_id = Column(Integer, ForeignKey('livros.id'))
    data_emprestimo = Column(DateTime, default=datetime.now)
    data_devolucao_prevista = Column(Date)
    data_devolucao_real = Column(Date, nullable=True)
    status = Column(String(20), default='ativo')
    observacoes = Column(Text)
    
    usuario = relationship("Usuario", back_populates="emprestimos")
    livro = relationship("Livro", back_populates="emprestimos")
    multa = relationship("Multa", back_populates="emprestimo", uselist=False)

class Reserva(Base):
    __tablename__ = 'reservas'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    livro_id = Column(Integer, ForeignKey('livros.id'))
    data_reserva = Column(DateTime, default=datetime.now)
    data_expiracao = Column(Date)
    status = Column(String(20), default='ativa')
    prioridade = Column(Integer, default=1)
    
    usuario = relationship("Usuario", back_populates="reservas")
    livro = relationship("Livro", back_populates="reservas")

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    cargo = Column(String(50))
    data_admissao = Column(Date, default=datetime.now)
    salario = Column(Float)
    ativo = Column(Boolean, default=True)

class Editora(Base):
    __tablename__ = 'editoras'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    endereco = Column(Text)
    telefone = Column(String(20))
    email = Column(String(100))
    data_cadastro = Column(DateTime, default=datetime.now)

class Multa(Base):
    __tablename__ = 'multas'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    emprestimo_id = Column(Integer, ForeignKey('emprestimos.id'))
    valor = Column(Float, default=0.0)
    data_multa = Column(DateTime, default=datetime.now)
    data_pagamento = Column(DateTime, nullable=True)
    status = Column(String(20), default='pendente')
    motivo = Column(Text)
    
    usuario = relationship("Usuario", back_populates="multas")
    emprestimo = relationship("Emprestimo", back_populates="multa")