from sqlalchemy import text
from database import DatabaseManager
from stored_procedures import StoredProcedures
from database_triggers import DatabaseTriggers

def main():
    try:
        db = DatabaseManager()
        db.create_tables()
        
        sp = StoredProcedures()
        sp.criar_stored_procedures()
        
        dt = DatabaseTriggers()
        dt.criar_triggers()
        
        demonstrar_sistema(db)
        
    except Exception as e:
        print(f"Erro: {e}")

def demonstrar_sistema(db):
    session = db.create_session()
    
    try:
        usuarios = session.execute(text("SELECT id, nome, email FROM usuarios"))
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}")
        
        livros = session.execute(text("SELECT id, titulo, quantidade_disponivel FROM livros"))
        for livro in livros:
            print(f"ID: {livro[0]}, Título: {livro[1]}, Disponível: {livro[2]}")
        
        relacionamentos = session.execute(text("""
            SELECT l.titulo, a.nome 
            FROM livro_autor la
            JOIN livros l ON la.livro_id = l.id
            JOIN autores a ON la.autor_id = a.id
        """))
        for rel in relacionamentos:
            print(f"Livro: {rel[0]}, Autor: {rel[1]}")
        
        resultado = session.execute(text("CALL registrar_emprestimo(1, 1, 14)"))
        for row in resultado:
            print(f"Resultado: {row[0]}")
            
        tabelas = session.execute(text("SHOW TABLES"))
        for tabela in tabelas:
            print(tabela[0])
        
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()