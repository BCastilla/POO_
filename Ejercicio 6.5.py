import html
import ipywidgets as widgets
from IPython.display import display


def html_alerta(mensaje):
    return ("<div style='background:#fdecea;color:#b71c1c;border:1px solid #f44336;"
            "border-radius:4px;padding:6px;margin:6px 0'>&#9888; "
            f"{html.escape(mensaje)}</div>")


class Vendedor:
    """Modela un vendedor con nombre, apellidos y edad."""
    EDAD_MINIMA_LABORAL = 18
    EDAD_MAXIMA = 120

    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = 0

    def imprimir(self):
        """Retorna el texto con los datos del vendedor (en el libro los imprime)."""
        return (f"Nombre del vendedor = {self.nombre}\n"
                f"Apellidos del vendedor = {self.apellidos}\n"
                f"Edad del vendedor = {self.edad}")

    def verificar_edad(self, edad):
        """Verifica que la edad sea apropiada; si no lo es, lanza la excepcion
        correspondiente (equivale a IllegalArgumentException)."""
        if edad < 0 or edad > Vendedor.EDAD_MAXIMA:
            raise ValueError("La edad no puede ser negativa ni mayor a 120.")
        if edad < Vendedor.EDAD_MINIMA_LABORAL:
            raise ValueError("El vendedor debe ser mayor de 18 años.")
        self.edad = edad


class VentanaPrincipal:
    """Interfaz grafica del ejercicio 6.5."""

    def __init__(self):
        estilo = {"description_width": "90px"}
        caja = widgets.Layout(width="300px")
        self.nombre = widgets.Text(description="Nombre:", style=estilo, layout=caja)
        self.apellidos = widgets.Text(description="Apellidos:", style=estilo, layout=caja)
        self.edad = widgets.Text(description="Edad:", style=estilo, layout=caja)
        self.crear = widgets.Button(description="Crear vendedor", button_style="success",
                                    layout=widgets.Layout(width="140px"))
        self.limpiar = widgets.Button(description="Limpiar", button_style="danger",
                                      layout=widgets.Layout(width="110px"))
        self.alerta = widgets.HTML("")
        self.resultado = widgets.HTML("")

        self.crear.on_click(self.action_performed)
        self.limpiar.on_click(self.action_performed)

        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Vendedor</h3>"),
             self.nombre, self.apellidos, self.edad,
             widgets.HBox([self.crear, self.limpiar]),
             self.alerta, self.resultado],
            layout=widgets.Layout(width="360px", border="1px solid #888",
                                  padding="12px"))

    def _crear_vendedor(self):
        """Lee los campos y crea el vendedor. Lanza ValueError si hay un problema."""
        nombre = self.nombre.value.strip()
        apellidos = self.apellidos.value.strip()
        if nombre == "" or apellidos == "":
            raise ValueError("El nombre y los apellidos son obligatorios.")
        try:
            edad = int(self.edad.value.strip())
        except ValueError:
            raise ValueError("La edad debe ser un número entero.") from None
        vendedor = Vendedor(nombre, apellidos)
        vendedor.verificar_edad(edad)
        return vendedor

    def action_performed(self, evento):
        if evento is self.crear:
            self.alerta.value = ""
            self.resultado.value = ""
            try:
                vendedor = self._crear_vendedor()
            except ValueError as error:
                self.alerta.value = html_alerta(str(error))
                return
            self.resultado.value = (
                "<pre style='background:#eef7ee;border:1px solid #8bc48b;"
                "border-radius:4px;padding:8px;margin:6px 0'>"
                f"{html.escape(vendedor.imprimir())}</pre>")
        if evento is self.limpiar:
            for campo in (self.nombre, self.apellidos, self.edad):
                campo.value = ""
            self.alerta.value = ""
            self.resultado.value = ""


class Principal:
    """Punto de ingreso al programa (equivale al metodo main)."""

    @staticmethod
    def main():
        mi_ventana_principal = VentanaPrincipal()
        display(mi_ventana_principal.contenedor)
        return mi_ventana_principal


mi_ventana = Principal.main()


def probar_modelo():
    v = Vendedor("Pedro", "Pérez")
    v.verificar_edad(18)
    assert v.edad == 18
    v.verificar_edad(120)
    assert v.edad == 120
    for edad, mensaje in [(17, "mayor de 18"), (0, "mayor de 18"),
                          (-5, "negativa ni mayor a 120"),
                          (121, "negativa ni mayor a 120")]:
        try:
            Vendedor("a", "b").verificar_edad(edad)
            raise AssertionError("debió lanzar ValueError")
        except ValueError as error:
            assert mensaje in str(error), (edad, str(error))
    print("OK  Modelo: verificar_edad lanza las excepciones correctas")


def probar_interfaz():
    v = VentanaPrincipal()
    v.nombre.value, v.apellidos.value = "Pedro", "Pérez"

    v.edad.value = "25"
    v.crear.click()
    assert "Edad del vendedor = 25" in v.resultado.value and v.alerta.value == ""

    v.edad.value = "17"
    v.crear.click()
    assert "debe ser mayor de 18 años" in v.alerta.value and v.resultado.value == ""

    v.edad.value = "130"
    v.crear.click()
    assert "negativa ni mayor a 120" in v.alerta.value

    v.edad.value = "abc"
    v.crear.click()
    assert "número entero" in v.alerta.value

    v.nombre.value = ""
    v.edad.value = "25"
    v.crear.click()
    assert "obligatorios" in v.alerta.value

    v.limpiar.click()
    assert v.nombre.value == "" and v.alerta.value == "" and v.resultado.value == ""
    print("OK  Interfaz: edad válida, <18, >120, no numérica, vacío y limpiar")


probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")
