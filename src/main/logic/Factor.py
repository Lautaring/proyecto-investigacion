from .Rol import Rol
from .Permeabilidad import Permeabilidad
from tkinter import messagebox


class Factor:
    #permeabilidad_1 : Permeabilidad luego modificar para pasar la permeabilidad como clase
    #rol_1 : Rol luego modificar para pasar el rol como clase
    def __init__(self, nombre, diversidad, masa_critica, orden, calidad, permeabilidad, coef_crecimiento, coef_mantenimiento, rol):
        self.nombre = nombre
        self.diversidad = diversidad
        self.masa_critica = masa_critica
        self.orden = orden
        self.calidad = calidad
        self.permeabilidad = permeabilidad
        self.coef_crecimiento = coef_crecimiento
        self.coef_mantenimiento = coef_mantenimiento
        self.rol = rol
