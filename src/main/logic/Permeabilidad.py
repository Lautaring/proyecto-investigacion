
class Permeabilidad:
    def __init__(self, Tipo, valor):
        self.tipo = Tipo
        self.valor = valor

    def Get_tipo(self):
        return self.tipo
    
    def Get_valor(self):
        return self.valor
    
    def Set_tipo(self, tipo_nuevo):
        self.tipo = tipo_nuevo

    def Set_valor(self, valor_nuevo):
        self.valor = valor_nuevo