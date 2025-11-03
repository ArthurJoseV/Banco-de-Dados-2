from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from base import Base, Usuario, Livro, Autor, Categoria, Emprestimo, Reserva, Funcionario, Editora, Multa
from datetime import datetime

class DatabaseManager:
    def __init__(self, database_url="mysql+pymysql://root:@localhost/biblioteca"):
        self.engine = create_engine(database_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_database(self):
        try:
            temp_engine = create_engine("mysql+pymysql://root:@localhost/")
            with temp_engine.connect() as conn:
                conn.execute(text("CREATE DATABASE IF NOT EXISTS biblioteca"))
            return True
        except Exception as e:
            return False
    
    def create_tables(self):
        if self.create_database():
            Base.metadata.create_all(self.engine)
        else:
            raise Exception("Não foi possível criar o database")
    
    def create_session(self):
        return self.Session()
    
    def add_sample_data(self):
        session = self.create_session()
        
        try:
            cat1 = Categoria(nome="Ficção Científica", descricao="Livros de ficção científica")
            cat2 = Categoria(nome="Romance", descricao="Romances literários")
            cat3 = Categoria(nome="Técnico", descricao="Livros técnicos e educacionais")
            
            autor1 = Autor(nome="Isaac Asimov", nacionalidade="Americano")
            autor2 = Autor(nome="George Orwell", nacionalidade="Britânico")
            autor3 = Autor(nome="J.K. Rowling", nacionalidade="Britânica")
            
            editora1 = Editora(nome="Editora Arqueiro", telefone="(11) 1234-5678")
            editora2 = Editora(nome="Companhia das Letras", telefone="(11) 9876-5432")
            
            livro1 = Livro(
                titulo="Fundação", 
                isbn="978-85-7542-823-9",
                ano_publicacao=1951,
                editora="Editora Arqueiro",
                quantidade_total=3,
                quantidade_disponivel=3
            )
            
            livro2 = Livro(
                titulo="1984",
                isbn="978-85-359-0277-8", 
                ano_publicacao=1949,
                editora="Companhia das Letras",
                quantidade_total=2,
                quantidade_disponivel=2
            )
            
            livro3 = Livro(
                titulo="Harry Potter e a Pedra Filosofal",
                isbn="978-85-325-2761-4",
                ano_publicacao=1997,
                editora="Editora Arqueiro",
                quantidade_total=5,
                quantidade_disponivel=5
            )
            
            livro1.autores.append(autor1)
            livro2.autores.append(autor2)
            livro3.autores.append(autor3)
            
            livro1.categorias.append(cat1)
            livro2.categorias.append(cat1)
            livro3.categorias.append(cat2)
            
            usuario1 = Usuario(
                nome="João Silva",
                email="joao.silva@email.com",
                telefone="(81) 99874-1475"
            )
            
            usuario2 = Usuario(
                nome="Maria Santos", 
                email="maria.santos@email.com",
                telefone="(87) 98754-2325"
            )
            
            funcionario1 = Funcionario(
                nome="Carlos Oliveira",
                email="carlos.oliveira@biblioteca.com",
                cargo="Bibliotecário",
                salario=3500.00
            )
            
            session.add_all([cat1, cat2, cat3, autor1, autor2, autor3, editora1, editora2, 
                           livro1, livro2, livro3, usuario1, usuario2, funcionario1])
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

if __name__ == "__main__":
    db = DatabaseManager()
    db.create_tables()
    db.add_sample_data()