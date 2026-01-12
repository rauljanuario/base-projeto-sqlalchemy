import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column 
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

engine = create_engine('sqlite://')

metadata_obj = MetaData()
user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(60)),
    Column('nickname', String(50), nullable=False)
)

user_prefs = Table(
    'user_prefs', metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100))
)

print("\nInfo da tabela users")
print(user_prefs.primary_key)
print(user_prefs.constraints)

print()
for table in metadata_obj.sorted_tables:
    print(table)


metadata_obj.create_all(engine)


financial_info = Table(
    'financial_info',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(100), nullable=False)
)

print("\nInfo da tabela financial_info")
print(financial_info.primary_key)
print(financial_info.constraints)


print("\nExecutando statement sql")

with engine.connect() as conn:
    # 1. Primeiro, vamos inserir um dado (corrigindo o SQL de 'select into' para 'insert into')
    # Usamos conn.execute e depois conn.commit() para salvar
    conn.execute(text("INSERT INTO user (user_id, user_name, email_address, nickname) VALUES (1, 'juliana', 'email@email.com', 'ju')"))
    conn.commit() # Importante para persistir os dados!

    # 2. Agora, vamos buscar os dados
    sql = text('SELECT * FROM user')
    result = conn.execute(sql)
    
    for row in result:
        print(f"ID: {row.user_id} - Nome: {row.user_name}")