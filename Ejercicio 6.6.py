import math
import ipywidgets as widgets
from IPython.display import display


class CalculosNumericos:
    """Calcula el logaritmo neperiano y la raiz cuadrada de un valor."""

    @staticmethod
    def calcular_logaritmo_neperiano(valor):
        """Retorna ln(valor). Si el valor no es positivo lanza ArithmeticError."""
        if valor <= 0:
            raise ArithmeticError("El valor debe ser un número positivo")
        return math.log(valor)

    @staticmethod
    def calcular_raiz_cuadrada(valor):
        """Retorna la raiz cuadrada. Si el valor es negativo lanza ArithmeticError."""
        if valor < 0:
            raise ArithmeticError("El valor debe ser un número positivo")
        return math.sqrt(valor)


class VentanaPrincipal:
    """Interfaz grafica del ejercicio 6.6."""

    def __init__(self):
        self.valor = widgets.Text(description="Valor numérico:",
                                  style={"description_width": "110px"},
                                  layout=widgets.Layout(width="320px"))
        self.calcular = widgets.Button(description="Calcular", button_style="success",
                                       layout=widgets.Layout(width="110px"))
        self.limpiar = widgets.Button(description="Limpiar", button_style="danger",
                                      layout=widgets.Layout(width="110px"))
        self.logaritmo = widgets.Label("Logaritmo neperiano = ")
        self.raiz = widgets.Label("Raíz cuadrada = ")

        self.calcular.on_click(self.action_performed)
        self.limpiar.on_click(self.action_performed)

        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Cálculos numéricos</h3>"),
             self.valor,
             widgets.HBox([self.calcular, self.limpiar]),
             self.logaritmo, self.raiz],
            layout=widgets.Layout(width="520px", border="1px solid #888",
                                  padding="12px"))

    @staticmethod
    def _leer_valor(texto):
        """Convierte el texto a numero; lanza ValueError si no es numerico."""
        try:
            valor = float(texto.strip().replace(",", "."))
        except ValueError:
            raise ValueError("no numerico") from None
        if not math.isfinite(valor):
            raise ValueError("no numerico")
        return valor

    def _ejecutar(self, funcion, nombre, texto):
        """Ejecuta un calculo con multiples catch (el orden importa: primero
        la excepcion aritmetica y luego la de formato)."""
        try:
            valor = self._leer_valor(texto)
            return f"{funcion(valor):.4f}"
        except ArithmeticError:
            return f"El valor debe ser un número positivo para calcular {nombre}"
        except ValueError:
            return f"El valor debe ser numérico para calcular {nombre}"

    def action_performed(self, evento):
        if evento is self.calcular:
            texto = self.valor.value
            self.logaritmo.value = "Logaritmo neperiano = " + self._ejecutar(
                CalculosNumericos.calcular_logaritmo_neperiano,
                "el logaritmo", texto)
            self.raiz.value = "Raíz cuadrada = " + self._ejecutar(
                CalculosNumericos.calcular_raiz_cuadrada,
                "la raíz cuadrada", texto)
        if evento is self.limpiar:
            self.valor.value = ""
            self.logaritmo.value = "Logaritmo neperiano = "
            self.raiz.value = "Raíz cuadrada = "


class Principal:
    """Punto de ingreso al programa (equivale al metodo main)."""

    @staticmethod
    def main():
        mi_ventana_principal = VentanaPrincipal()
        display(mi_ventana_principal.contenedor)
        return mi_ventana_principal


mi_ventana = Principal.main()


def probar_modelo():
    assert abs(CalculosNumericos.calcular_logaritmo_neperiano(math.e) - 1.0) < 1e-9
    assert abs(CalculosNumericos.calcular_raiz_cuadrada(81) - 9.0) < 1e-9
    assert CalculosNumericos.calcular_raiz_cuadrada(0) == 0.0
    for f, valor in [(CalculosNumericos.calcular_logaritmo_neperiano, -1),
                     (CalculosNumericos.calcular_logaritmo_neperiano, 0),
                     (CalculosNumericos.calcular_raiz_cuadrada, -4)]:
        try:
            f(valor)
            raise AssertionError("debió lanzar ArithmeticError")
        except ArithmeticError:
            pass
    print("OK  Modelo: logaritmo y raíz cuadrada, con sus excepciones")


def probar_interfaz():
    v = VentanaPrincipal()

    v.valor.value = "100"
    v.calcular.click()
    assert v.logaritmo.value == "Logaritmo neperiano = 4.6052"
    assert v.raiz.value == "Raíz cuadrada = 10.0000"

    v.valor.value = "-4"
    v.calcular.click()
    assert "positivo para calcular el logaritmo" in v.logaritmo.value
    assert "positivo para calcular la raíz cuadrada" in v.raiz.value

    v.valor.value = "0"
    v.calcular.click()
    assert "positivo para calcular el logaritmo" in v.logaritmo.value
    assert v.raiz.value == "Raíz cuadrada = 0.0000"

    v.valor.value = "abc"
    v.calcular.click()
    assert "numérico para calcular el logaritmo" in v.logaritmo.value
    assert "numérico para calcular la raíz cuadrada" in v.raiz.value

    v.valor.value = "2,25"
    v.calcular.click()
    assert v.raiz.value == "Raíz cuadrada = 1.5000"

    v.limpiar.click()
    assert v.valor.value == "" and v.logaritmo.value == "Logaritmo neperiano = "
    print("OK  Interfaz: positivo, negativo, cero, no numérico, coma y limpiar")


probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")
