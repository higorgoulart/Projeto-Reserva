from model.reserva import Reserva
from model.enums.tipo_quarto_enum import TipoQuarto
from model.enums.status_reserva_enum import Status
from model.enums.tipo_relatorio_enum import TipoRelatorio
import service.service
import re
service = service.service


def validar_cpf(cpf):
  if cpf == "":
    return { "valido": False, "mensagem": "CPF não pode ser vazio." }

  if not re.search("([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2})", cpf):
    return { "valido": False, "mensagem": "CPF inválido" }
  
  return { "valido": True, "mensagem": "" }

def validar_numero(numero_input):
  numero = 0

  if numero_input == "":
    return { "valido": False, "mensagem": "{0} não pode ser vazio." }
  
  try:
    numero = int(numero_input)
  except:
    return { "valido": False, "mensagem": "{0} inválido." }

  if numero <= 0:
    return { "valido": False, "mensagem": "{0} não pode ser menor ou igual a zero" }
  
  return { "valido": True, "mensagem": "" }

def validar_tipo_quarto(tipo_quarto):  
  if tipo_quarto == "":
    return { "valido": False, "mensagem": "Tipo de quarto não pode ser vazio." }
  
  try:
    TipoQuarto[tipo_quarto.upper()]
  except:
    return { "valido": False, "mensagem": "Tipo de quarto inválido." }
 
  return { "valido": True, "mensagem": "" }

def validar_status(status):
  if status == "":
    return { "valido": False, "mensagem": "Status não pode ser vazio." }
  
  try:
    Status[status.upper()]
  except:
    return { "valido": False, "mensagem": "Status inválido." }
 
  return { "valido": True, "mensagem": "" }

def obter_texto_reserva(reserva: Reserva):
  return ("Nome: " + reserva.nome + ", CPF: " + reserva.cpf + " (" + str(reserva.numero_dias) + " dias, " + str(reserva.numero_pessoas) + " pessoas, Quarto " + TipoQuarto[reserva.tipo_quarto].value["tipo"] + ", R$ " + str(reserva.valor) + ", Status: " + Status[reserva.status].value + ")")

def obter_numeros_cpf(cpf):
  digitos = ""
      
  for digito in re.findall("\d+", cpf):
    digitos = digitos + digito

  return digitos

def selecionar_reserva(lista_reservas):
  opcao = 0

  try:  
    if len(lista_reservas) > 1:
      for item in lista_reservas:
        print(lista_reservas.index(item) + 1, "-", obter_texto_reserva(item))

      try:
        i = int(input("Digite o número da reserva que deseja selecionar: "))

        if i > len(lista_reservas):
          raise

        opcao = i - 1
      except:
        print("Opção inválida.")
        return None
        
    return lista_reservas[opcao]
  except:
    print("Não foi possível encontrar nenhuma reserva disponível com este CPF. ")


class ReservaController:
  def realizar_cadastro(): 
    try:
      print("--Cadastro de reserva-- \n")
      print("Digite os valores para os campos:")
    
      nome = input("Nome da pessoa titular: ")

      if nome == "":
        raise Exception("Nome não pode ser vazio.") 
      
      cpf = input("CPF do titular: ")

      retorno = validar_cpf(cpf)

      if not retorno["valido"]:
        raise Exception(retorno["mensagem"])
      
      numero_pessoas = input("Número de pessoas: ")

      retorno = validar_numero(numero_pessoas)
      
      if not retorno["valido"]:
        raise Exception(retorno["mensagem"].format("Número de pessoas"))
      
      numero_dias = input("Número de dias: ")

      retorno = validar_numero(numero_dias)
      
      if not retorno["valido"]:
        raise Exception(retorno["mensagem"].format("Número de dias"))
      
      tipo_quarto = input("Tipo do quarto desejado (S - Standard / D - Deluxe / P - Premium): ")

      retorno = validar_tipo_quarto(tipo_quarto)
      
      if not retorno["valido"]:
        raise Exception(retorno["mensagem"])
      
      reserva = Reserva(
        nome, 
        obter_numeros_cpf(cpf), 
        int(numero_pessoas), 
        int(numero_dias), 
        tipo_quarto.upper())
 
      service.salvar_cadastro(reserva)
      
      print("Cadastro realizado com sucesso!")
    except Exception as e:
      print(e)
      
  def atualizar_cadastro():
    try:
      print("--Atualização de cadastro-- \n")
      
      cpf = obter_numeros_cpf(input("Insira o CPF: "))
      
      lista_reserva = service.obter_cadastro_por_cpf(cpf, Status.R.name)
  
      reserva = selecionar_reserva(lista_reserva)
  
      if reserva is None:
        return

      numero_pessoas = input("Número de pessoas: ")

      retorno = validar_numero(numero_pessoas)
      
      if not retorno["valido"]:
        raise Exception(retorno["mensagem"].format("Número de pessoas"))
      
      numero_dias = input("Número de dias: ")

      retorno = validar_numero(numero_dias)
      
      if not retorno["valido"]:
        raise Exception(retorno["mensagem"].format("Número de dias"))
      
      tipo_quarto = input("Tipo do quarto desejado (S - Standard / D - Deluxe / P - Premium): ")

      retorno = validar_tipo_quarto(tipo_quarto)
      
      if not retorno["valido"]:
        raise Exception(retorno["mensagem"])
      
      status = input("Status (R - Reservado / C - Cancelado / A - Ativo / F - Finalizado): ")

      retorno = validar_status(status)
      
      if not retorno["valido"]:
        raise Exception(retorno["mensagem"])

      reserva_atualizada = Reserva(
        reserva.nome, 
        cpf, 
        int(numero_pessoas), 
        int(numero_dias), 
        tipo_quarto.upper(), 
        None, 
        status.upper(), 
        reserva.rowid)

      service.atualizar_cadastro(reserva_atualizada)
      
      print("Atualização realizado com sucesso!")
    except Exception as e:
      print(e)
    
  def realizar_checkin():
    try:
      print("--Check in-- \n")
      
      cpf = obter_numeros_cpf(input("Insira o CPF: "))
      
      lista_reserva = service.obter_cadastro_por_cpf(cpf, Status.R.name)
    
      reserva = selecionar_reserva(lista_reserva)

      if reserva is None:
        return
  
      reserva.status = Status.A.name
      
      service.atualizar_cadastro(reserva)
      
      print("Check in realizado com sucesso! ")
    except Exception as e:
      print(e)

  def realizar_checkout():
    try:
      print("--Check out-- \n")
      
      cpf = obter_numeros_cpf(input("Insira o CPF: "))
      
      lista_reserva = service.obter_cadastro_por_cpf(cpf, Status.A.name)
  
      reserva = selecionar_reserva(lista_reserva)

      if reserva is None:
        return
  
      reserva.status = Status.F.name
      
      service.atualizar_cadastro(reserva)
      
      print("Check out realizado com sucesso! ")
    except Exception as e:
      print(e)

  def obter_relatorio(tipo_relatorio: TipoRelatorio):
    try:
      lista_reservas = []

      if tipo_relatorio == TipoRelatorio.StatusR:
        lista_reservas = service.obter_cadastro_por_status(Status.R)
      elif tipo_relatorio == TipoRelatorio.StatusC:
        lista_reservas = service.obter_cadastro_por_status(Status.C)
      elif tipo_relatorio == TipoRelatorio.StatusA:
        lista_reservas = service.obter_cadastro_por_status(Status.A)
      elif tipo_relatorio == TipoRelatorio.StatusF:
        lista_reservas = service.obter_cadastro_por_status(Status.F)
      elif tipo_relatorio == TipoRelatorio.PorCPF:
        cpf = obter_numeros_cpf(input("Insira o CPF: "))
        lista_reservas = service.obter_cadastro_por_cpf(cpf)
      elif tipo_relatorio == TipoRelatorio.SomaTotal:
        total = (service.obter_total_finalizados())
        print("A soma total de reservas finalizdas é de R$ " + str(total))
        return

      if len(lista_reservas) <= 0:
        raise Exception("Não foi possível encontrar nenhuma reserva. ")
      
      for item in lista_reservas:
        print(obter_texto_reserva(item))
    except Exception as e:
      print(e)