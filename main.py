from sqlalchemy import text
from database import DatabaseManager
from stored_procedures import StoredProcedures
from database_triggers import DatabaseTriggers

def main():
    db = DatabaseManager()
    
    db.create_tables()
    
    sp = StoredProcedures()
    sp.criar_stored_procedures()
    dt = DatabaseTriggers()
    dt.criar_triggers()
    teste_sistema(db)

def teste_sistema(db):
    session = db.create_session()
    
    try:
        usuarios = session.execute(text("SELECT id, nome FROM usuarios"))
        for user in usuarios:
            print(f"{user[0]} - {user[1]}")
        
        livros = session.execute(text("SELECT id, titulo FROM livros"))
        for livro in livros:
            print(f"{livro[0]} - {livro[1]}")
        
        resultado = session.execute(text("CALL registrar_emprestimo(1, 1, 14)"))
        for row in resultado:
            print(row[0])
            
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
