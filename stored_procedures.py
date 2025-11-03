# procedures/stored_procedures.py
from database import DatabaseManager
from sqlalchemy import text

class StoredProcedures:
    def __init__(self):
        self.db = DatabaseManager()
    
    def criar_stored_procedures(self):
        """Cria as 4 stored procedures obrigatórias"""
        session = self.db.create_session()
        
        try:
            # PROCEDURE 1: Registrar empréstimo com validações
            procedure1 = """
            CREATE PROCEDURE IF NOT EXISTS registrar_emprestimo(
                IN p_usuario_id INT,
                IN p_livro_id INT,
                IN p_dias_emprestimo INT
            )
            BEGIN
                DECLARE v_disponivel INT;
                DECLARE v_emprestimos_ativos INT;
                DECLARE v_multa_pendente INT;
                
                SELECT quantidade_disponivel INTO v_disponivel 
                FROM livros WHERE id = p_livro_id;
                
                SELECT COUNT(*) INTO v_emprestimos_ativos 
                FROM emprestimos 
                WHERE usuario_id = p_usuario_id AND status = 'ativo';
                
                SELECT COUNT(*) INTO v_multa_pendente 
                FROM multas 
                WHERE usuario_id = p_usuario_id AND status = 'pendente';
                
                IF v_disponivel > 0 THEN
                    IF v_emprestimos_ativos < 5 THEN
                        IF v_multa_pendente = 0 THEN
                            INSERT INTO emprestimos (
                                usuario_id, livro_id, data_emprestimo, 
                                data_devolucao_prevista, status
                            ) VALUES (
                                p_usuario_id, p_livro_id, NOW(),
                                DATE_ADD(NOW(), INTERVAL p_dias_emprestimo DAY), 'ativo'
                            );
                            
                            UPDATE livros 
                            SET quantidade_disponivel = quantidade_disponivel - 1 
                            WHERE id = p_livro_id;
                            
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
            
            # PROCEDURE 2: Devolver livro e calcular multa
            procedure2 = """
            CREATE PROCEDURE IF NOT EXISTS devolver_livro(
                IN p_emprestimo_id INT
            )
            BEGIN
                DECLARE v_data_prevista DATE;
                DECLARE v_livro_id INT;
                DECLARE v_dias_atraso INT;
                DECLARE v_valor_multa DECIMAL(10,2);
                
                SELECT data_devolucao_prevista, livro_id 
                INTO v_data_prevista, v_livro_id
                FROM emprestimos 
                WHERE id = p_emprestimo_id;
                
                SET v_dias_atraso = DATEDIFF(NOW(), v_data_prevista);
                
                IF v_dias_atraso > 0 THEN
                    SET v_valor_multa = v_dias_atraso * 2.50;
                    
                    INSERT INTO multas (
                        usuario_id, emprestimo_id, valor, 
                        data_multa, status, motivo
                    ) SELECT 
                        usuario_id, p_emprestimo_id, v_valor_multa,
                        NOW(), 'pendente', CONCAT('Atraso de ', v_dias_atraso, ' dias')
                    FROM emprestimos WHERE id = p_emprestimo_id;
                    
                    UPDATE emprestimos 
                    SET status = 'atrasado', data_devolucao_real = NOW()
                    WHERE id = p_emprestimo_id;
                    
                    SELECT CONCAT('Devolução com atraso. Multa: R$ ', v_valor_multa) AS resultado;
                ELSE
                    UPDATE emprestimos 
                    SET status = 'finalizado', data_devolucao_real = NOW()
                    WHERE id = p_emprestimo_id;
                    
                    SELECT 'Devolução realizada com sucesso' AS resultado;
                END IF;
                
                UPDATE livros 
                SET quantidade_disponivel = quantidade_disponivel + 1 
                WHERE id = v_livro_id;
            END
            """
            
            # PROCEDURE 3: Relatório de livros mais emprestados
            procedure3 = """
            CREATE PROCEDURE IF NOT EXISTS relatorio_livros_mais_emprestados(
                IN p_mes INT,
                IN p_ano INT
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
                    MONTH(emp.data_emprestimo) = p_mes 
                    AND YEAR(emp.data_emprestimo) = p_ano
                GROUP BY l.id, l.titulo, l.isbn, l.editora, l.quantidade_disponivel
                ORDER BY total_emprestimos DESC
                LIMIT 10;
            END
            """
            
            # PROCEDURE 4: Estatísticas mensais
            procedure4 = """
            CREATE PROCEDURE IF NOT EXISTS estatisticas_mensais(
                IN p_mes INT,
                IN p_ano INT
            )
            BEGIN
                SELECT 
                    (SELECT COUNT(*) FROM emprestimos 
                     WHERE MONTH(data_emprestimo) = p_mes AND YEAR(data_emprestimo) = p_ano) as total_emprestimos,
                    
                    (SELECT COUNT(*) FROM reservas 
                     WHERE MONTH(data_reserva) = p_mes AND YEAR(data_reserva) = p_ano) as total_reservas,
                    
                    (SELECT COUNT(*) FROM multas 
                     WHERE MONTH(data_multa) = p_mes AND YEAR(data_multa) = p_ano) as total_multas,
                    
                    (SELECT COALESCE(SUM(valor), 0) FROM multas 
                     WHERE MONTH(data_multa) = p_mes AND YEAR(data_multa) = p_ano) as valor_total_multas,
                    
                    (SELECT titulo FROM livros l 
                     JOIN emprestimos e ON l.id = e.livro_id 
                     WHERE MONTH(e.data_emprestimo) = p_mes AND YEAR(e.data_emprestimo) = p_ano 
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
    sp.criar_stored_procedures()