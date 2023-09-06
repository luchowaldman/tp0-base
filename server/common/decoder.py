
from common.utils import Bet


class BetDecoder:
    @staticmethod
    def decode(encoded_text):
        # Extraer campos de la cadena codificada        
        agencia = int(encoded_text[:5])
        nombre = encoded_text[5:35].strip()  # Cambiar de 15 a 35 caracteres y eliminar espacios en blanco adicionales
        apellido = encoded_text[35:65].strip()  # Cambiar de 15 a 35 caracteres y eliminar espacios en blanco adicionales
        dni = encoded_text[65:73]
        nacimiento = encoded_text[73:83].strip()
        numero = int(encoded_text[83:87])
        # Crear una instancia de la clase Bet con los campos extraídos
        bet = Bet(agencia, nombre, apellido, dni, nacimiento, numero)
        return bet
        
        
    @staticmethod
    def tamanio_apuesta():        
        return 87
        
        

    @staticmethod
    def decode_vector(text):
        # Dividir el texto en pedazos de 87 caracteres
        chunks = [text[i:i+87] for i in range(0, len(text), 87)]

        # Decodificar cada fragmento y almacenarlos en una lista de objetos Bet
        decoded_bets = []
        for chunk in chunks:
            decoded_bet = BetDecoder.decode(chunk)
            decoded_bets.append(decoded_bet)

        return decoded_bets
