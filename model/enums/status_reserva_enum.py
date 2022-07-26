from enum import Enum


class Status(Enum):
  R = "Reservado"
  C = "Cancelado"
  A = "Ativo"
  F = "Finalizado"