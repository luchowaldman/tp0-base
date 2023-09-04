
from common.utils import Bet


class BetDecoder:
    @staticmethod
    def decode(encoded_text):
        # Extraer campos de la cadena codificada
        agencia = int(encoded_text[:5])
        nombre = encoded_text[5:15].strip()
        apellido = encoded_text[15:25].strip()
        dni = encoded_text[25:33]
        nacimiento = encoded_text[33:43].strip()
        numero = int(encoded_text[43:47])

        # Crear una instancia de la clase Bet con los campos extraídos
        bet = Bet(agencia, nombre, apellido, dni, nacimiento, numero)

        return bet
