import html
import ipywidgets as widgets
from IPython.display import display


class PruebaExcepciones:
    """Lanza diferentes excepciones en situaciones especificas del programa.
    Los mensajes ayudan a identificar la porcion de codigo que se ejecuto."""

    @staticmethod
    def ejecutar_principal():
        """Equivale al metodo main del libro (dos bloques try)."""
        salida = []


        try:
            salida.append("Ingresando al primer try")
            divisor = 0
            cociente = 10000 / divisor
            salida.append("Despues de la division")
        except ArithmeticError:
            salida.append("División por cero")
        finally:
            salida.append("Ingresando al primer finally")


        try:
            salida.append("Ingresando al segundo try")
            objeto = None
            objeto.toString()
            salida.append("Imprimiendo objeto")
        except ArithmeticError:
            salida.append("División por cero")
        except Exception:
            salida.append("Ocurrió una excepción")
        finally:
            salida.append("Ingresando al segundo finally")
        return salida

    @staticmethod
    def ejecutar_fuera_limite():
        """Ejercicio propuesto 1: indice de un String fuera del limite."""
        salida = []
        try:
            texto = "Programación"
            caracter = texto[14]
            salida.append(caracter)
        except IndexError:
            salida.append("Indice de string por fuera del límite")
        return salida

    @staticmethod
    def ejecutar_formato_numero():
        """Ejercicio propuesto 2: conversion de texto a entero."""
        salida = []
        try:
            numero = int("Número")
            salida.append(str(numero))
        except ValueError:
            salida.append("Excepción de formato de número")
        finally:
            salida.append("Ingresando al finally")
        return salida


class VentanaPrincipal:
    """Interfaz grafica del ejercicio 6.4."""

    def __init__(self):
        self._experimentos = {
            "principal": PruebaExcepciones.ejecutar_principal,
            "limite": PruebaExcepciones.ejecutar_fuera_limite,
            "numero": PruebaExcepciones.ejecutar_formato_numero,
        }
        self.experimento = widgets.Dropdown(
            options=[("Ejercicio 6.4: PruebaExcepciones (dos try)", "principal"),
                     ("Propuesto 1: índice fuera de límite", "limite"),
                     ("Propuesto 2: formato de número", "numero")],
            description="Ejecutar:", style={"description_width": "70px"},
            layout=widgets.Layout(width="440px"))
        self.ejecutar = widgets.Button(description="Ejecutar", button_style="success",
                                       layout=widgets.Layout(width="110px"))
        self.limpiar = widgets.Button(description="Limpiar", button_style="danger",
                                      layout=widgets.Layout(width="110px"))
        self.salida = widgets.HTML(self._formatear([]))

        self.ejecutar.on_click(self.action_performed)
        self.limpiar.on_click(self.action_performed)

        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Excepciones</h3>"),
             self.experimento,
             widgets.HBox([self.ejecutar, self.limpiar]),
             widgets.HTML("<b>Salida del programa:</b>"),
             self.salida],
            layout=widgets.Layout(width="480px", border="1px solid #888",
                                  padding="12px"))

    @staticmethod
    def _formatear(lineas):
        texto = "\n".join(lineas) if lineas else "(sin salida)"
        return ("<pre style='background:#f4f4f4;border:1px solid #ccc;"
                "border-radius:4px;padding:8px;margin:4px 0'>"
                f"{html.escape(texto)}</pre>")

    def action_performed(self, evento):
        if evento is self.ejecutar:
            lineas = self._experimentos[self.experimento.value]()
            self.salida.value = self._formatear(lineas)
        if evento is self.limpiar:
            self.salida.value = self._formatear([])


class Principal:
    """Punto de ingreso al programa (equivale al metodo main)."""

    @staticmethod
    def main():
        mi_ventana_principal = VentanaPrincipal()
        display(mi_ventana_principal.contenedor)
        return mi_ventana_principal


mi_ventana = Principal.main()


def probar_modelo():
    assert PruebaExcepciones.ejecutar_principal() == [
        "Ingresando al primer try", "División por cero",
        "Ingresando al primer finally", "Ingresando al segundo try",
        "Ocurrió una excepción", "Ingresando al segundo finally"]
    assert PruebaExcepciones.ejecutar_fuera_limite() == [
        "Indice de string por fuera del límite"]
    assert PruebaExcepciones.ejecutar_formato_numero() == [
        "Excepción de formato de número", "Ingresando al finally"]
    print("OK  Modelo: la salida coincide con la del libro")


def probar_interfaz():
    v = VentanaPrincipal()
    v.ejecutar.click()
    assert "Ingresando al primer finally" in v.salida.value
    assert "Ocurrió una excepción" in v.salida.value
    assert "Imprimiendo objeto" not in v.salida.value
    v.experimento.value = "limite"
    v.ejecutar.click()
    assert "por fuera del límite" in v.salida.value
    v.experimento.value = "numero"
    v.ejecutar.click()
    assert "formato de número" in v.salida.value
    v.limpiar.click()
    assert "(sin salida)" in v.salida.value
    print("OK  Interfaz: ejecutar los tres experimentos y limpiar")


probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")
