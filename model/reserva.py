from model.enums.tipo_quarto_enum import TipoQuarto
from model.enums.status_reserva_enum import Status


class Reserva:
  def __init__(self, 
              nome: str, 
              cpf: str, 
              numero_pessoas: int,
              numero_dias: int, 
              tipo_quarto: str,
              valor: int = None,
              status: str = None,
              rowid: int = 0):
    self.nome = nome
    self.cpf = cpf
    self.numero_dias = numero_dias
    self.numero_pessoas = numero_pessoas
    self.tipo_quarto = tipo_quarto

    if valor is None:
      self.valor = TipoQuarto[tipo_quarto].value["valor"] * numero_dias * numero_pessoas
    else:
      self.valor = valor

    if status is None:
      self.status = Status.R.name
    else:
      self.status = status

    self.rowid = rowid