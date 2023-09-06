
from common.utils import Bet
from common.mensaje import Mensaje, TipoMensaje


class BetDecoder:
    def decode(encoded_text, agencia):
        # Extraer campos de la cadena codificada
        nombre = encoded_text[0:30].strip()  # Cambiar de 5 a 30 caracteres y eliminar espacios en blanco adicionales
        apellido = encoded_text[30:60].strip()  #
        dni = encoded_text[60:68]
        nacimiento = encoded_text[68:78].strip()
        numero = int(encoded_text[78:82])
        # Crear una instancia de la clase Bet con los campos extraídos
        bet = Bet(agencia, nombre, apellido, dni, nacimiento, numero)
        return bet

        
        
    @staticmethod
    def tamanio_apuesta():        
        return 82
        
        

    @staticmethod
    def decode_vector(text, agencia):
        # Dividir el texto en pedazos de tamanio_apuesta() caracteres
        chunks = [text[i:i+BetDecoder.tamanio_apuesta()] for i in range(0, len(text), BetDecoder.tamanio_apuesta())]

        # Decodificar cada fragmento y almacenarlos en una lista de objetos Bet
        decoded_bets = []
        for chunk in chunks:
            decoded_bet = BetDecoder.decode(chunk, agencia)
            decoded_bets.append(decoded_bet)

        return decoded_bets

    def decode_mensaje(msg):
        if msg.startswith("A"):
            agencia = int(msg[1:])
            return Mensaje(TipoMensaje.ENVIA_APUESTAS, agencia)
        if msg.startswith("F"):
            agencia = int(msg[1:])
            return Mensaje(TipoMensaje.FIN_ENVIO, agencia)
        
                
        