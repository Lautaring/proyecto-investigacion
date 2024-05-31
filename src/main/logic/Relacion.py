from Factor import Factor
from Permeabilidad import Permeabilidad
from Vinculo import Vinculo

class Relacion:
    def __init__(self, factor_1 : Factor, permeabilidad_1 : Permeabilidad, vinculo_1 : Vinculo):
        self.factor = factor_1
        self.permeabilidad = permeabilidad_1
        self.vinculo = vinculo_1
        
    def Get_factor(self):
        return self.factor
    
    def Get_permeabilidad(self):
        return self.permeabilidad

    def Get_vinculo(self):
        return self.vinculo