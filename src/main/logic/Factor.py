from .Rol import Rol


class Factor:
    def __init__(self, nombre, diversidad, masa_critica, orden, calidad, coeficiente_crecimiento, coeficiente_mantenimiento, rol_1 : Rol):
        self.nombre = nombre
        self.diversidad = diversidad
        self.masa_critica = masa_critica
        self.orden = orden
        self.calidad = calidad
        self.coeficiente_crecimiento = coeficiente_crecimiento
        self.coeficiente_mantenimiento = coeficiente_mantenimiento
        self.rol = rol_1