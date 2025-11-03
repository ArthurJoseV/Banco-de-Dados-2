from database import DatabaseManager
from sqlalchemy import text

class DatabaseTriggers:
    def __init__(self):
        self.db = DatabaseManager()
    
    def criar_triggers(self):
        session = self.db.create_session()
        
        try:
            
            trigger1 = """
            CREATE TRIGGER IF NOT EXISTS impedir_emprestimo_multa
            BEFORE INSERT ON emprestimos
            FOR EACH ROW
            BEGIN
                DECLARE multa_pendente INT;
                
                SELECT COUNT(*) INTO multa_pendente 
                FROM multas 
                WHERE usuario_id = NEW.usuario_id AND status = 'pendente';
                
                IF multa_pendente > 0 THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Usuário possui multas pendentes. Empréstimo não permitido.';
                END IF;
            END
            """
            
           
            trigger2 = """
            CREATE TRIGGER IF NOT EXISTS att_quantidade_emprestimo
            AFTER INSERT ON emprestimos
            FOR EACH ROW
            BEGIN
                UPDATE livros 
                SET quantidade_disponivel = quantidade_disponivel - 1 
                WHERE id = NEW.livro_id;
            END
            """
            
           
            trigger3 = """
            CREATE TRIGGER IF NOT EXISTS validar_livro
            BEFORE INSERT ON livros
            FOR EACH ROW
            BEGIN
                DECLARE current_year INT;
                SET current_year = YEAR(CURDATE());
                
                IF NEW.ano_publicacao > current_year THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Ano de publicação não pode ser no futuro';
                END IF;
                
                IF NEW.quantidade_total < 0 THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Quantidade total não pode ser negativa';
                END IF;
                
                IF NEW.quantidade_disponivel < 0 THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Quantidade disponível não pode ser negativa';
                END IF;
                
                IF NEW.quantidade_disponivel > NEW.quantidade_total THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Quantidade disponível não pode ser maior que quantidade total';
                END IF;
            END
            """
            
            session.execute(text("DROP TRIGGER IF EXISTS impedir_emprestimo_multa"))
            session.execute(text("DROP TRIGGER IF EXISTS att_quantidade_emprestimo"))
            session.execute(text("DROP TRIGGER IF EXISTS validar_livro"))
            session.execute(text(trigger1))
            session.execute(text(trigger2))
            session.execute(text(trigger3))
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

if __name__ == "__main__":
    dt = DatabaseTriggers()
    dt.criar_triggers()
