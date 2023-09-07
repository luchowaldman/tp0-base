from common.utils import Bet

class BetEncoder:

    @staticmethod
    def FinApuestasOk():
        return "O".encode('utf-8')
    
    @staticmethod
    def SinSorteo():
        return "N".encode('utf-8')
    
    @staticmethod
    def ConSorteo(ganadores: list[Bet]):
        tot_ganadores = str(len(ganadores)).zfill(5)[:5]
        concatenated_dniss = ""
        # Recorremos la lista de apuestas y concatenamos los DNIs
        for bet in ganadores:
            concatenated_dniss += str(bet.document).zfill(8)[:8]        
        return f"R{tot_ganadores}{concatenated_dniss}".encode('utf-8')
    