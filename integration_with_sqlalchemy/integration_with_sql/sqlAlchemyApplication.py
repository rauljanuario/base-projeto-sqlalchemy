import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import Column 
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    #Atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")
    
    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"
    

print(User.__tablename__)

# Conexao com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Investiga o schema do banco de dados
# inspetor_engine = inspect(engine)

# print(inspetor_engine.has_table("user_account"))
# print(inspetor_engine.get_table_names())
# print(inspetor_engine.default_schema_name)


with Session(engine) as session:
    raul = User(
        name = 'raul',
        fullname = 'Raul Januario',
        address = [Address(email_address='raul@email.com')]
    )

    sandy = User(
        name = 'sandy',
        fullname = 'Sandy Junior',
        address = [Address(email_address='sandy@email.com'),
                   Address(email_address='sandyjunior@gmail.com')]
    )

    patrick = User(name='patrick', fullname='Patrick Cardoso')

    # Inserindo dados no BD(persistindo informações)
    session.add_all([raul, sandy, patrick])
    session.commit()

# Consulta de recuperação de informações
print("\nRecuperando usuários a partir de uma condição de filtragem")

stmt = select(User).where(User.name.in_(['raul']))
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
for address in session.scalars(stmt_address):
    print(address)

# recuperando dados de forma ordenada

stmt_order = select(User).order_by(User.fullname.desc())
print("\ndados ordenados recuperados")
for result in session.scalars(stmt_order):
    print(result)

# recuperando dados a partir do join
stmt_join = select(User.fullname, Address.email_address).join_from(User, Address)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
print("\nTotal de instâncias em user")
for result in session.scalars(stmt_count):
    print(result)

# encerrando a session
session.close()