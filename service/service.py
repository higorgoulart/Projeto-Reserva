from infra.conexao import obter_conexao
from model.reserva import Reserva
from model.enums.status_reserva_enum import Status


conexao = obter_conexao()

cursor = conexao.cursor()

def salvar_cadastro(reserva: Reserva):
  query = """INSERT INTO reserva 
              (nome, 
              cpf, 
              numero_pessoas, 
              numero_dias, 
              tipo_quarto,
              valor, 
              status) 
            VALUES(?, ?, ?, ?, ?, ?, ?)"""

  valores = (reserva.nome, reserva.cpf, reserva.numero_pessoas, reserva.numero_dias, reserva.tipo_quarto, reserva.valor, reserva.status)

  cursor.execute(query, valores)

  conexao.commit()
  
def atualizar_cadastro(reserva: Reserva):  
  query = """UPDATE reserva SET
              numero_pessoas = ?, 
              numero_dias = ?, 
              tipo_quarto = ?, 
              valor = ?, 
              status = ? 
              WHERE rowid = ?"""

  valores = (reserva.numero_pessoas, reserva.numero_dias, reserva.tipo_quarto, reserva.valor, reserva.status, reserva.rowid)

  cursor.execute(query, valores)

  conexao.commit()

def obter_cadastro_por_cpf(cpf: str, status: str = ""):
  query = """SELECT 
              nome, 
              cpf, 
              numero_pessoas, 
              numero_dias, 
              tipo_quarto, 
              valor, 
              status, 
              rowid 
            FROM reserva WHERE cpf = ? """
  
  valores = [cpf]

  if status != "":
    query += """AND status = ?"""
    valores.append(status)
  
  cursor.execute(query, valores)

  rows = cursor.fetchall()

  lista_reservas = []

  for row in rows:
    lista_reservas.append(Reserva(row[0], row[1], row[2], row[3], 
                                  row[4], row[5], row[6], row[7]))

  return lista_reservas

def obter_cadastro_por_status(status: Status): 
  query = """SELECT 
              nome, 
              cpf, 
              numero_pessoas, 
              numero_dias, 
              tipo_quarto, 
              valor, 
              status, 
              rowid 
            FROM reserva WHERE status = ?"""
  
  valores = [status.name]
 
  cursor.execute(query, valores)
  rows = cursor.fetchall()

  lista_reservas = []
  
  for row in rows:
    lista_reservas.append(Reserva(row[0], row[1], row[2], row[3], 
                                  row[4], row[5], row[6], row[7]))

  return lista_reservas

def obter_total_finalizados(): 
  query = """SELECT SUM(valor) FROM reserva WHERE status = 'F'"""

  cursor.execute(query)
  
  rows = cursor.fetchall()

  return rows[0][0]