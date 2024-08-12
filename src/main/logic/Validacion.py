from tkinter import messagebox


class Validacion:
    
    def validar_campos(self):
        """Valida que todos los campos del formulario estén llenos y que los valores sean correctos."""
        # Obtener los valores de los campos
        nombre = self.factor_name_entry.get().strip()
        diversidad = self.diversity_entry.get().strip()
        masa_critica = self.masa_critica_entry.get().strip()
        orden = self.orden_entry.get().strip()
        calidad = self.calidad_entry.get().strip()
        coef_crecimiento = self.coef_crecimiento_entry.get().strip()
        coef_mantenimiento = self.coef_mantenimiento_entry.get().strip()

        # Verificar que ninguno de los campos esté vacío
        if not nombre:
            messagebox.showerror("Error", "El nombre del factor no puede estar vacío.")
            return False
        if not diversidad:
            messagebox.showerror("Error", "La diversidad no puede estar vacía.")
            return False
        if not masa_critica:
            messagebox.showerror("Error", "La masa crítica no puede estar vacía.")
            return False
        if not orden:
            messagebox.showerror("Error", "El orden no puede estar vacío.")
            return False
        if not calidad:
            messagebox.showerror("Error", "La calidad no puede estar vacía.")
            return False
        if not coef_crecimiento:
            messagebox.showerror("Error", "El coeficiente de crecimiento no puede estar vacío.")
            return False
        if not coef_mantenimiento:
            messagebox.showerror("Error", "El coeficiente de mantenimiento no puede estar vacío.")
            return False

        # Verificar que los valores numéricos sean válidos
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