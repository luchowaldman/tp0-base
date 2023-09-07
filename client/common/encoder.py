from common.apuesta import Apuesta

class ApuestaEncoder:
    @staticmethod
    def encode(apuesta):
        # Verificar y ajustar la longitud de cada campo
        nombre = apuesta.nombre[:30].ljust(30)
        apellido = apuesta.apellido[:30].ljust(30)
        dni = apuesta.dni.zfill(8)[:8]
        nacimiento = apuesta.nacimiento[:10].ljust(10)
        numero = apuesta.numero.zfill(4)[:4]

        # Combinar los campos en una cadena codificada
        encoded_apuesta = f"{nombre}{apellido}{dni}{nacimiento}{numero}"

        return encoded_apuesta

    @staticmethod
    def encode_vector(apuestas: [Apuesta], agencia):
        # Aplicar la función encode() a cada apuesta en el vector
        encoded_apuestas = [ApuestaEncoder.encode(apuesta) for apuesta in apuestas]
    
        # Usar join para concatenar las respuestas en una sola cadena
        encoded_vector = "".join(encoded_apuestas)
        agencia = str(agencia).zfill(5)[:5]
        total_enviados = str(len(apuestas)).zfill(5)[:5]
    
        return f"A{agencia}{total_enviados}{encoded_vector}"
    

    @staticmethod
    def encode_finapuestas(agencia):
        # Aplicar la función encode() a cada apuesta en el vector
        agencia = str(agencia).zfill(5)[:5]
        return f"F{agencia}"
    

    @staticmethod
    def encode_consultaganador(agencia):
        # Aplicar la función encode() a cada apuesta en el vector
        agencia = str(agencia).zfill(5)[:5]
        return f"C{agencia}"