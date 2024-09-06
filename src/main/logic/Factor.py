from .Rol import Rol
from .Permeabilidad import Permeabilidad
from tkinter import messagebox


class Factor:
    def __init__(self, nombre, diversidad, masa_critica, orden, calidad, permeabilidad_1 : Permeabilidad, coeficiente_crecimiento, coeficiente_mantenimiento, rol_1 : Rol):
        self.nombre = nombre
        self.diversidad = diversidad
        self.masa_critica = masa_critica
        self.orden_social_fisico_simbolico = orden
        self.calidad = calidad
        self.permeabilidad = permeabilidad_1
        self.coeficiente_crecimiento = coeficiente_crecimiento
        self.coeficiente_mantenimiento = coeficiente_mantenimiento
        self.rol = rol_1

    #Podria


    def Validar_campos(self):
        # Verificar que ninguno de los campos esté vacío
        if not self.nombre:
            messagebox.showerror("Error", "El nombre del factor no puede estar vacío.")
            return False
        if not self.diversidad:
            messagebox.showerror("Error", "La diversidad no puede estar vacía.")
            return False
        if not self.masa_critica:
            messagebox.showerror("Error", "La masa crítica no puede estar vacía.")
            return False
        if not self.orden_social_fisico_simbolico:
            messagebox.showerror("Error", "El orden no puede estar vacío.")
            return False
        if not self.calidad:
            messagebox.showerror("Error", "La calidad no puede estar vacía.")
            return False
        if not self.coeficiente_crecimiento:
            messagebox.showerror("Error", "El coeficiente de crecimiento no puede estar vacío.")
            return False
        if not self.coeficiente_mantenimiento:
            messagebox.showerror("Error", "El coeficiente de mantenimiento no puede estar vacío.")
            return False

        # Verificar que los valores numéricos sean válidos
        try:
            float(self.diversidad)
            float(self.masa_critica)
            float(self.orden_social_fisico_simbolico)
            float(self.calidad)
            float(self.coeficiente_crecimiento)
            float(self.coeficiente_mantenimiento)
        except ValueError:
            messagebox.showerror("Error", "Todos los valores numéricos deben ser válidos.")
            return False

        return True