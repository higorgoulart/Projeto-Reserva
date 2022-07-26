from enum import Enum


class TipoQuarto(Enum):
  S = {"tipo": "Standard", "valor": 100}
  D = {"tipo": "Deluxe", "valor": 200}
  P = {"tipo": "Premium", "valor": 300}