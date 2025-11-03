PROJETO DE BANCO DE DADOS 2 - IFPE PAULISTA


Sistema de gestão de bibliotecas

#Para rodá-lo, será necessário:

- Python 3.10+
- SQLAlchemy -> pip install sqlalchemy pymysql
- datetime (para manipulação de datas) -> database_url = "mysql+pymysql://root:@localhost/biblioteca"
- MySQL ou Postgresql

- 1. Clone o repositório

- git clone https://github.com/seu-usuario/sistema-biblioteca.git
cd sistema-biblioteca

2. Instale as dependências
   
- ## ⚙️ Estrutura do Projeto

O sistema foi desenvolvido utilizando o padrão **ORM (Object-Relational Mapping)** do SQLAlchemy.  
Cada classe Python representa uma **tabela** no banco de dados

3. Configure o banco de dados

python database.py        # Cria database e tabelas
python stored_procedures.py  # Cria procedures
python triggers.py        # Cria triggers

4. Execute a instalação

from database import DatabaseManager

# Cria e configura o banco
db = DatabaseManager()
db.create_tables()
db.add_sample_data()  # Dados de exempl
