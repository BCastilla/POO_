import math
import ipywidgets as widgets
from IPython.display import display

# Clase Notas 
class Notas:
    TOTAL_NOTAS = 5

    def __init__(self):
        # Atributo que identifica la lista de notas
        self.lista_notas = [0.0] * Notas.TOTAL_NOTAS

    def calcular_promedio(self):
        """Retorna el promedio de las notas."""
        suma = 0.0
        for nota in self.lista_notas:  # recorre TODA la lista
            suma += nota
        return suma / len(self.lista_notas)

    def calcular_desviacion(self):
        """Retorna la desviacion estandar (poblacional, como en el libro)."""
        prom = self.calcular_promedio()
        suma = 0.0
        for nota in self.lista_notas:
            suma += math.pow(nota - prom, 2)
        return math.sqrt(suma / len(self.lista_notas))

    def calcular_menor(self):
        """Retorna la menor nota."""
        menor = self.lista_notas[0]
        for nota in self.lista_notas:
            if nota < menor:
                menor = nota
        return menor

    def calcular_mayor(self):
        """Retorna la mayor nota."""
        mayor = self.lista_notas[0]
        for nota in self.lista_notas:
            if nota > mayor:
                mayor = nota
        return mayor

# Clase VentanaPrincipal
class VentanaPrincipal:
    """Interfaz grafica"""
    NOTA_MINIMA = 0.0  
    NOTA_MAXIMA = 5.0

    def __init__(self):
        estilo = {"description_width": "60px"}
        caja = widgets.Layout(width="230px")

        # Etiquetas y campos de texto de cada nota
        self.campos_nota = [
            widgets.Text(description=f"Nota {i}:", placeholder="0.0 - 5.0",
                         style=estilo, layout=caja)
            for i in range(1, Notas.TOTAL_NOTAS + 1)
        ]

        # Botones
        self.calcular = widgets.Button(description="Calcular", button_style="success",
                                       layout=widgets.Layout(width="110px"))
        self.limpiar = widgets.Button(description="Limpiar", button_style="danger",
                                      layout=widgets.Layout(width="110px"))

        # Zona de alertas (equivale a JOptionPane)
        self.alerta = widgets.HTML("")

        # Etiquetas de resultados (parte inferior de la ventana)
        self.promedio = widgets.Label("Promedio = ")
        self.desviacion = widgets.Label("Desviación estándar = ")
        self.mayor = widgets.Label("Nota mayor = ")
        self.menor = widgets.Label("Nota menor = ")

        # Se registra el "listener" de cada boton (equivale a addActionListener)
        self.calcular.on_click(self.action_performed)
        self.limpiar.on_click(self.action_performed)

        # Contenedor principal (equivale a getContentPane)
        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Notas</h3>")]
            + self.campos_nota
            + [widgets.HBox([self.calcular, self.limpiar]), self.alerta,
               self.promedio, self.desviacion, self.mayor, self.menor],
            layout=widgets.Layout(width="300px", border="1px solid #888",
                                  padding="12px")
        )

    # ---------- utilidades ----------
    def _mostrar_alerta(self, mensaje):
        self.alerta.value = ("<div style='background:#fdecea;color:#b71c1c;"
                             "border:1px solid #f44336;border-radius:4px;"
                             f"padding:6px;margin:6px 0'>&#9888; {mensaje}</div>")

    def _limpiar_resultados(self):
        self.promedio.value = "Promedio = "
        self.desviacion.value = "Desviación estándar = "
        self.mayor.value = "Nota mayor = "
        self.menor.value = "Nota menor = "

    def _leer_notas(self):
        """Lee y valida los campos. Lanza ValueError con el mensaje de alerta."""
        notas = Notas()
        for i, campo in enumerate(self.campos_nota):
            texto = campo.value.strip()
            if texto == "":
                raise ValueError(f"La Nota {i + 1} no ha sido ingresada. "
                                 "Las cinco notas son obligatorias.")
            try:
                valor = float(texto.replace(",", "."))
            except ValueError:
                raise ValueError(f"La Nota {i + 1} (“{texto}”) no es un valor "
                                 "numérico.") from None
            if not math.isfinite(valor):
                raise ValueError(f"La Nota {i + 1} (“{texto}”) no es un valor "
                                 "numérico válido.")
            if not (self.NOTA_MINIMA <= valor <= self.NOTA_MAXIMA):
                raise ValueError(f"La Nota {i + 1} debe estar entre "
                                 f"{self.NOTA_MINIMA:g} y {self.NOTA_MAXIMA:g}.")
            notas.lista_notas[i] = valor
        return notas

    # ---------- gestion de eventos ----------
    def action_performed(self, evento):
        """Gestiona los eventos de los botones (equivale a actionPerformed)."""
        if evento is self.calcular:
            self.alerta.value = ""
            try:
                notas = self._leer_notas()
            except ValueError as error:
                self._limpiar_resultados()
                self._mostrar_alerta(str(error))
                return
            self.promedio.value = f"Promedio = {notas.calcular_promedio():.2f}"
            self.desviacion.value = (f"Desviación estándar = "
                                     f"{notas.calcular_desviacion():.2f}")
            self.mayor.value = f"Nota mayor = {notas.calcular_mayor():.2f}"
            self.menor.value = f"Nota menor = {notas.calcular_menor():.2f}"

        if evento is self.limpiar:
            for campo in self.campos_nota:
                campo.value = ""
            self.alerta.value = ""
            self._limpiar_resultados()


# CELDA 4 - Clase Principal 
class Principal:
    """Punto de ingreso al programa (equivale al metodo main)."""

    @staticmethod
    def main():
        mi_ventana_principal = VentanaPrincipal()   # crea la ventana
        display(mi_ventana_principal.contenedor)    # la hace visible
        return mi_ventana_principal

mi_ventana = Principal.main()

# Verificacion automatica
def probar_modelo():
    n = Notas()
    n.lista_notas = [3.0, 4.0, 5.0, 2.0, 1.0]
    assert abs(n.calcular_promedio() - 3.0) < 1e-9
    assert abs(n.calcular_desviacion() - math.sqrt(2)) < 1e-9
    assert n.calcular_mayor() == 5.0 and n.calcular_menor() == 1.0
    # La primera nota SI se incluye en el promedio
    n.lista_notas = [5.0, 0.0, 0.0, 0.0, 0.0]
    assert abs(n.calcular_promedio() - 1.0) < 1e-9
    print("OK  Modelo Notas: promedio, desviación, mayor y menor")

def probar_interfaz():
    v = VentanaPrincipal()          # ventana de prueba (no se muestra)

    # 1) Datos validos
    for campo, valor in zip(v.campos_nota, ["3", "4", "5", "2", "1"]):
        campo.value = valor
    v.calcular.click()
    assert v.promedio.value == "Promedio = 3.00"
    assert v.desviacion.value == "Desviación estándar = 1.41"
    assert v.mayor.value == "Nota mayor = 5.00"
    assert v.menor.value == "Nota menor = 1.00"
    assert v.alerta.value == ""
    print("OK  Calcular con datos válidos")

    # 2) Dato NO numerico -> alerta
    v.campos_nota[2].value = "abc"
    v.calcular.click()
    assert "no es un valor numérico" in v.alerta.value
    assert v.promedio.value == "Promedio = "
    print("OK  Alerta por dato no numérico")

    # 3) Nota vacia -> alerta
    v.campos_nota[2].value = ""
    v.calcular.click()
    assert "no ha sido ingresada" in v.alerta.value
    print("OK  Alerta por nota no ingresada")

    # 4) Fuera de rango -> alerta
    v.campos_nota[2].value = "7"
    v.calcular.click()
    assert "entre 0 y 5" in v.alerta.value
    print("OK  Alerta por nota fuera de rango")

    # 5) Limpiar
    v.limpiar.click()
    assert all(c.value == "" for c in v.campos_nota) and v.alerta.value == ""
    print("OK  Botón Limpiar")

probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")
