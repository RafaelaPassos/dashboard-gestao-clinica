import sqlite3
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DE AMBIENTE E DADOS FICTÍCIOS
# ---------------------------------------------------------
# O Faker gera nomes, datas e locais realistas em Português do Brasil.
fake = Faker('pt_BR')

pasta_banco = os.path.join('..', 'banco_de_dados')
pasta_dashboard = os.path.join('..', 'dashboard')
os.makedirs(pasta_banco, exist_ok=True)
os.makedirs(pasta_dashboard, exist_ok=True)

caminho_banco = os.path.join(pasta_banco, 'clinica.db')
conexao = sqlite3.connect(caminho_banco)

# ---------------------------------------------------------
# 2. GERANDO TABELAS DE DIMENSÃO (Profissionais e Pacientes)
# ---------------------------------------------------------
# Profissionais: Define a lista fixa de especialidades para analisar receita futura.
especialidades = ['Pediatria', 'Clínica Geral', 'Ortodontia', 'Cardiologia', 'Dermatologia']
profissionais = []

for i in range(1, 11):
    profissionais.append({
        'id_profissional': i,
        'nome': f"Dr(a). {fake.name()}",
        'especialidade': random.choice(especialidades),
        'registro_conselho': f"CRM/CRO-{random.randint(10000, 99999)}"
    })
df_profissionais = pd.DataFrame(profissionais)

# Pacientes: Tabela de perfil demográfico (200 registros).
pacientes = []
for i in range(1, 201):
    pacientes.append({
        'id_paciente': i,
        'nome': fake.name(),
        'data_nascimento': fake.date_of_birth(minimum_age=1, maximum_age=85).strftime('%Y-%m-%d'),
        'genero': random.choice(['M', 'F']),
        'cidade': random.choice(['Rio de Janeiro', 'Niterói', 'São Gonçalo', 'Duque de Caxias'])
    })
df_pacientes = pd.DataFrame(pacientes)

# ---------------------------------------------------------
# 3. GERANDO A TABELA FATO (Consultas)
# ---------------------------------------------------------
# Simulação de 1.500 eventos (consultas) distribuídos em 365 dias.
consultas = []
data_inicial = datetime.now() - timedelta(days=365)

for i in range(1500):
    dias_aleatorios = random.randint(0, 365)
    hora_aleatoria = random.randint(8, 17)
    minuto_aleatorio = random.choice([0, 30])
    
    data_consulta = data_inicial + timedelta(days=dias_aleatorios)
    data_hora_final = data_consulta.replace(hour=hora_aleatoria, minute=minuto_aleatorio, second=0)
    
    # REGRA DE NEGÓCIO: Define 18% de probabilidade estatística para o estado 'Faltou'.
    # Isso simula o problema real de absenteísmo (No-Show) na clínica.
    status = 'Faltou' if random.random() < 0.18 else 'Compareceu'
    
    consultas.append({
        'id_consulta': i + 1,
        'id_paciente': random.randint(1, 200),
        'id_profissional': random.randint(1, 10),
        'data_hora': data_hora_final.strftime('%Y-%m-%d %H:%M:%S'),
        'status': status,
        'valor': round(random.uniform(150.0, 450.0), 2)
    })
df_consultas = pd.DataFrame(consultas)

# ---------------------------------------------------------
# 4. PERSISTÊNCIA DOS DADOS (SQL + CSV)
# ---------------------------------------------------------
# Armazena a estrutura no banco relacional SQLite.
df_profissionais.to_sql('Profissionais', conexao, if_exists='replace', index=False)
df_pacientes.to_sql('Pacientes', conexao, if_exists='replace', index=False)
df_consultas.to_sql('Consultas', conexao, if_exists='replace', index=False)
conexao.close()

# Exporta em CSV com codificação utf-8-sig para leitura direta no Power BI.
df_profissionais.to_csv(os.path.join(pasta_dashboard, 'profissionais.csv'), index=False, encoding='utf-8-sig')
df_pacientes.to_csv(os.path.join(pasta_dashboard, 'pacientes.csv'), index=False, encoding='utf-8-sig')
df_consultas.to_csv(os.path.join(pasta_dashboard, 'consultas.csv'), index=False, encoding='utf-8-sig')

print("Processo concluído com sucesso: Banco SQLite e arquivos CSV atualizados!")