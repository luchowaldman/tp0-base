from common.apuesta import Apuesta

class ApuestaEncoder:
    @staticmethod
    def encode(apuesta):
        # Verificar y ajustar la longitud de cada campo
        agencia = str(apuesta.agencia).zfill(5)[:5]
        nombre = apuesta.nombre[:10].ljust(30)
        apellido = apuesta.apellido[:10].ljust(30)
        dni = apuesta.dni.zfill(8)[:8]
        nacimiento = apuesta.nacimiento[:10].ljust(10)
        numero = apuesta.numero.zfill(4)[:4]

        # Combinar los campos en una cadena codificada
        encoded_apuesta = f"{agencia}{nombre}{apellido}{dni}{nacimiento}{numero}"

        # 87 Caracteres en total

        return encoded_apuesta

    @staticmethod
    def encode_vector(apuestas: [Apuesta]):
        # Aplicar la función encode() a cada apuesta en el vector
        encoded_apuestas = [ApuestaEncoder.encode(apuesta) for apuesta in apuestas]
    
        # Usar join para concatenar las respuestas en una sola cadena
        encoded_vector = "".join(encoded_apuestas)
        total_enviados = str(len(apuestas)).zfill(5)[:5]
    
        return f"A{total_enviados}{encoded_vector}"
    

    @staticmethod
    def encode_finapuestas(agencia):
        # Aplicar la función encode() a cada apuesta en el vector
        agencia = str(agencia).zfill(5)[:5]
        return f"F{agencia}"