from controller.reserva_controller import ReservaController
from model.enums.tipo_relatorio_enum import TipoRelatorio
from infra.conexao import criar_conexao, finalizar_conexao
from utils.utils import Utils
from utils.cores import Cores

criar_conexao()

while True:
  print("1 - Cadastrar uma reserva")
  print("2 - Entrada do cliente (Check in)")
  print("3 - Saída do cliente (Check out)")
  print("4 - Alterar reserva")
  print("5 - Relatórios")
  print("6 - Sair")

  try:
    opcao = int(input("Digite sua escolha: "))
 
    Utils.limpar_console()
  
    if opcao == 1:
      ReservaController.realizar_cadastro()
    elif opcao == 2:
      ReservaController.realizar_checkin()
    elif opcao == 3:
      ReservaController.realizar_checkout()
    elif opcao == 4:
      ReservaController.atualizar_cadastro()
    elif opcao == 5:
      print("1 - Relatório de todas as reservas com status R.")
      print("2 - Relatório de todas as reservas com status C.")
      print("3 - Relatório de todas as reservas com status A.")
      print("4 - Relatório de todas as reservas com status F.")
      print("5 - Relatório total recebido (somar valor de todas as reservas finalizadas)")
      print("6 – Relatório de reserva por pessoa (Pesquisa por CPF)")

      tipo_relatorio = int(input("Digite sua escolha: "))

      ReservaController.obter_relatorio(TipoRelatorio(tipo_relatorio))
    elif opcao == 6:
      finalizar_conexao()
      break
    else:
      raise

    print("Pressione enter para repetir. ")
    input("")
    
  except:
    Utils.limpar_console()
    print(Cores.amarelo + "Opção inválida. (Pressione enter para repetir)")
    input("")    
    print(Cores.branco)
  
  Utils.limpar_console()