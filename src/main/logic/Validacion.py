from tkinter import messagebox

class Validacion:
    
    def validar_campos(self, nombre, diversidad, masa_critica, orden, calidad, coef_crecimiento, coef_mantenimiento):
        """Valida que todos los campos del formulario estén llenos y que los valores sean correctos."""
        
        # Verificación de campos vacíos
        if not nombre.strip():
            messagebox.showerror("Error", "El nombre del factor no puede estar vacío.")
            return False
        if not diversidad.strip():
            messagebox.showerror("Error", "La diversidad no puede estar vacía.")
            return False
        if not masa_critica.strip():
            messagebox.showerror("Error", "La masa crítica no puede estar vacía.")
            return False
        if not orden.strip():
            messagebox.showerror("Error", "El orden no puede estar vacío.")
            return False
        if not calidad.strip():
            messagebox.showerror("Error", "La calidad no puede estar vacía.")
            return False
        if not coef_crecimiento.strip():
            messagebox.showerror("Error", "El coeficiente de crecimiento no puede estar vacío.")
            return False
        if not coef_mantenimiento.strip():
            messagebox.showerror("Error", "El coeficiente de mantenimiento no puede estar vacío.")
            return False

        # Verificación de que los valores numéricos sean válidos
        try:
            float(diversidad)
            float(masa_critica)
            float(orden)
            float(calidad)
            float(coef_crecimiento)
            float(coef_mantenimiento)
        except ValueError:
            messagebox.showerror("Error", "Todos los valores numéricos deben ser válidos.")
            return False

        return True
