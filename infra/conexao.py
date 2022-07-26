import sqlite3
from sqlite3 import Error


caminho_db = "infra/database/database"

conexao = sqlite3.connect(caminho_db)
cursor = conexao.cursor()

def obter_conexao():
  return conexao
  
def criar_conexao(db_file = caminho_db):
  try:
    cursor.execute("""CREATE TABLE IF NOT EXISTS reserva(
                        nome TEXT NOT NULL, 
                        cpf TEXT NOT NULL, 
                        numero_pessoas INTEGER NOT NULL, 
                        numero_dias INTEGER NOT NULL,  
                        tipo_quarto TEXT NOT NULL, 
                        valor INTEGER NOT NULL,
                        status TEXT NOT NULL)""")    
  except Error as e:
    print(e)

def finalizar_conexao():
  conexao.close()