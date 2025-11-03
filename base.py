from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Table, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()
livro_autor = Table('livro_autor', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('livro_id', Integer, ForeignKey('livros.id')),
    Column('autor_id', Integer, ForeignKey('autores.id')))

livro_categoria = Table('livro_categoria', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('livro_id', Integer, ForeignKey('livros.id')),
    Column('categoria_id', Integer, ForeignKey('categorias.id')))

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100))
    telefone = Column(String(15))
    
    emprestimos = relationship("Emprestimo", backref="usuario")
    reservas = relationship("Reserva", backref="usuario")
    multas = relationship("Multa", backref="usuario")
    
class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(150))
    ano_publicacao = Column(Integer)
    editora = Column(String(80))
    quantidade_total = Column(Integer)
    quantidade_disponivel = Column(Integer)

    autores = relationship("Autor", secondary=livro_autor, backref="livros")
    categorias = relationship("Categoria", secondary=livro_categoria, backref="livros")
    emprestimos = relationship("Emprestimo", backref="livro")
    reservas = relationship("Reserva", backref="livro")

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    nacionalidade = Column(String(30))

class Categoria(Base):
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(40))
    descricao = Column(Text)
    
class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    livro_id = Column(Integer, ForeignKey('livros.id'))
    data_emprestimo = Column(DateTime)
    data_devolucao_prevista = Column(Date)
    data_devolucao_real = Column(Date)
    status = Column(String(15))
    observacoes = Column(Text)
    
    multa = relationship("Multa", uselist=False, backref="emprestimo")

class Reserva(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    livro_id = Column(Integer, ForeignKey('livros.id'))
    data_reserva = Column(DateTime)
    expiracao = Column(Date)
    status = Column(String(15))
    
class Funcionario(Base):
    __tablename__ = 'funcionarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    email = Column(String(100))
    cargo = Column(String(40))
    salario = Column(Float)

class Editora(Base):
    __tablename__ = 'editoras'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    telefone = Column(String(15))
    email = Column(String(90))
class Multa(Base):
    __tablename__ = 'multas'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    emprestimo_id = Column(Integer, ForeignKey('emprestimos.id'))
    valor = Column(Float)
    dia_multa = Column(DateTime)
    pagamento_multa = Column(DateTime)
    status = Column(String(20))
    motivo = Column(Text)
