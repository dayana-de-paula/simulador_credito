from app.database import Base, motor
from app.models import Simulacao

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=motor)
print("Tabelas criadas com sucesso!")
