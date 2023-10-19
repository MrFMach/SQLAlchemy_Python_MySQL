# IMPORTANTE: Instalar o driver mysql-connector-python, mesmo não utilizando a biblioteca no código:
# pip install mysql-connector-python

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import time

sgbd = 'mysql'
driver = 'mysqlconnector'
usuario = 'root'
senha = 'rootpassword'
host = 'localhost'
banco = 'db_sqlalchemy'

# Criar uma instância do 'engine' (motor) para se conectar ao banco de dados
engine = create_engine(f'{sgbd}+{driver}://{usuario}:{senha}@{host}/{banco}')

# Criar uma classe Base para definir os modelos (tabelas)
Base = declarative_base()

# Definir um modelo (tabela)
class TbNumAleatorio(Base):
    __tablename__ = 'numeros_aleatorios'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    num_aleatorio = Column(Integer)
    horario = Column(String(8))

# Excluir a tabela (se quiser começar de novo)
# TbNumAleatorio.__table__.drop(engine)

# Criar a tabela no banco de dados (só precisa ser feito uma vez)
Base.metadata.create_all(engine)

# Criar uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

for i in range(5):
    numero = random.randint(1000, 9999)
    agora = datetime.now()
    hora = agora.strftime("%H:%M:%S")

    # Exemplos de inserção de dados
    novo_numero = TbNumAleatorio(num_aleatorio=numero, horario=hora)
    session.add(novo_numero)
    session.commit()
    print(f'Registro inserido: {hora}')
    time.sleep(1)

# Exemplos de consulta de dados
filtro = session.query(TbNumAleatorio).filter_by(id= '3').first()
print('======================')
print('Consulta com filtro (ID = 3)')
print(f'ID: {filtro.id} | Número: {filtro.num_aleatorio} | Hora: {filtro.horario}')

print('======================')
print('Consultar tudo:')
tudo = session.query(TbNumAleatorio).all()
for num in tudo:
    print(f'{num.id} | {num.num_aleatorio} | {num.horario}')

# Fechar a sessão
session.close()