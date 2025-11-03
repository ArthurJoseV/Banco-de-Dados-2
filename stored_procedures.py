from database import DatabaseManager
from sqlalchemy import text

class StoredProcedures:
    def __init__(self):
        self.db = DatabaseManager()
    
    def criar_sprocedures(self):
        session = self.db.create_session()
        try:
            procedure1 = """
            CREATE PROCEDURE IF NOT EXISTS registrar_emprestimo(
                IN usuario_id INT,
                IN livro_id INT,
                IN dias_emprestimo INT
            )
            BEGIN
                DECLARE disponivel INT;
                DECLARE emprestimos_ativos INT;
                DECLARE multa_pendente INT;
                
                SELECT quantidade_disponivel INTO disponivel 
                FROM livros WHERE id = livro_id;
                
                SELECT COUNT(*) INTO emprestimos_ativos 
                FROM emprestimos 
                WHERE usuario_id = usuario_id AND status = 'ativo';
                
                SELECT COUNT(*) INTO multa_pendente 
                FROM multas 
                WHERE usuario_id = usuario_id AND status = 'pendente';
                
                IF disponivel > 0 THEN
                    IF emprestimos_ativos < 5 THEN
                        IF multa_pendente = 0 THEN
                            INSERT INTO emprestimos (
                                usuario_id, livro_id, data_emprestimo, 
                                data_devolucao_prevista, status
                            ) VALUES (
                                usuario_id, livro_id, NOW(),
                                DATE_ADD(NOW(), INTERVAL p_dias_emprestimo DAY), 'ativo'
                            );
                            
                            UPDATE livros 
                            SET quantidade_disponivel = quantidade_disponivel - 1 
                            WHERE id = livro_id;
                            
                            SELECT 'Empréstimo registrado com sucesso' AS resultado;
                        ELSE
                            SELECT 'Usuário possui multas pendentes' AS resultado;
                        END IF;
                    ELSE
                        SELECT 'Usuário atingiu limite de empréstimos' AS resultado;
                    END IF;
                ELSE
                    SELECT 'Livro não disponível' AS resultado;
                END IF;
            END
            """
            procedure2 = """
            CREATE PROCEDURE IF NOT EXISTS devolver_livro(
                IN emprestimo_id INT
            )
            BEGIN
                DECLARE data_prevista DATE;
                DECLARE livro_id INT;
                DECLARE dias_atraso INT;
                DECLARE valor_multa DECIMAL(10,2);
                
                SELECT data_devolucao_prevista, livro_id 
                INTO data_prevista, livro_id
                FROM emprestimos 
                WHERE id = emprestimo_id;
                
                SET dias_atraso = DATEDIFF(NOW(), v_data_prevista);
                
                IF dias_atraso > 0 THEN
                    SET valor_multa = dias_atraso * 1.50;
                    
                    INSERT INTO multas (
                        usuario_id, emprestimo_id, valor, 
                        data_multa, status, motivo
                    ) SELECT 
                        usuario_id, emprestimo_id, valor_multa,
                        NOW(), 'pendente', CONCAT('Atraso de ', dias_atraso, ' dias')
                    FROM emprestimos WHERE id = emprestimo_id;
                    
                    UPDATE emprestimos 
                    SET status = 'atrasado', data_devolucao_real = NOW()
                    WHERE id = emprestimo_id;
                    
                    SELECT CONCAT('Devolução com atraso. Multa: R$ ', valor_multa) AS resultado;
                ELSE
                    UPDATE emprestimos 
                    SET status = 'finalizado', data_devolucao_real = NOW()
                    WHERE id = emprestimo_id;
                    
                    SELECT 'Devolução realizada com sucesso' AS resultado;
                END IF;
                
                UPDATE livros 
                SET quantidade_disponivel = quantidade_disponivel + 1 
                WHERE id = livro_id;
            END
            """
            procedure3 = """
            CREATE PROCEDURE IF NOT EXISTS relatorio_lvrs_mais_emprestados(
                IN mes INT,
                IN ano INT
            )
            BEGIN
                SELECT 
                    l.titulo,
                    l.isbn,
                    l.editora,
                    COUNT(emp.id) as total_emprestimos,
                    l.quantidade_disponivel as copias_disponiveis
                FROM livros l
                LEFT JOIN emprestimos emp ON l.id = emp.livro_id
                WHERE 
                    MONTH(emp.data_emprestimo) = mes 
                    AND YEAR(emp.data_emprestimo) = ano
                GROUP BY l.id, l.titulo, l.isbn, l.editora, l.quantidade_disponivel
                ORDER BY total_emprestimos DESC
                LIMIT 10;
            END
            """

            procedure4 = """
            CREATE PROCEDURE IF NOT EXISTS estatisticas_mensais(
                IN mes INT,
                IN ano INT
            )
            BEGIN
                SELECT 
                    (SELECT COUNT(*) FROM emprestimos 
                     WHERE MONTH(data_emprestimo) = mes AND YEAR(data_emprestimo) = ano) as total_emprestimos,
                    
                    (SELECT COUNT(*) FROM reservas 
                     WHERE MONTH(data_reserva) = mes AND YEAR(data_reserva) = ano) as total_reservas,
                    
                    (SELECT COUNT(*) FROM multas 
                     WHERE MONTH(data_multa) = mes AND YEAR(data_multa) = ano) as total_multas,
                    
                    (SELECT COALESCE(SUM(valor), 0) FROM multas 
                     WHERE MONTH(data_multa) = mes AND YEAR(data_multa) = ano) as valor_total_multas,
                    
                    (SELECT titulo FROM livros l 
                     JOIN emprestimos e ON l.id = e.livro_id 
                     WHERE MONTH(e.data_emprestimo) = mes AND YEAR(e.data_emprestimo) = ano 
                     GROUP BY l.id, l.titulo 
                     ORDER BY COUNT(*) DESC LIMIT 1) as livro_mais_emprestado;
            END
            """
            
            session.execute(text("DROP PROCEDURE IF EXISTS registrar_emprestimo"))
            session.execute(text("DROP PROCEDURE IF EXISTS devolver_livro"))
            session.execute(text("DROP PROCEDURE IF EXISTS relatorio_livros_mais_emprestados"))
            session.execute(text("DROP PROCEDURE IF EXISTS estatisticas_mensais"))
            session.execute(text(procedure1))
            session.execute(text(procedure2))
            session.execute(text(procedure3))
            session.execute(text(procedure4))
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
if __name__ == "__main__":
    sp = StoredProcedures()
    sp.criar_sprocedures()
