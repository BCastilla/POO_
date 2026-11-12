import html
import ipywidgets as widgets
from IPython.display import display


def html_alerta(mensaje):
    return ("<div style='background:#fdecea;color:#b71c1c;border:1px solid #f44336;"
            "border-radius:4px;padding:6px;margin:6px 0'>&#9888; "
            f"{html.escape(mensaje)}</div>")


class LeerArchivo:
    """Lee los datos presentes en un archivo de texto (.txt)."""

    CONTENIDO_EJEMPLO = ("Programación Orientada a Objetos\n"
                         "Universidad Nacional de Colombia\n"
                         "Ejercicio 6.8: lectura de archivos\n")

    @staticmethod
    def leer(nombre_archivo):
        """Lee el archivo linea a linea y retorna la lista de lineas.
        Lanza OSError (o UnicodeDecodeError) si no se puede leer."""
        lineas = []
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            linea = archivo.readline()
            while linea != "":
                lineas.append(linea.rstrip("\n"))
                linea = archivo.readline()
        return lineas

    @staticmethod
    def a_mayusculas(lineas):
        """Ejercicio propuesto: convierte las lineas a mayusculas."""
        return [linea.upper() for linea in lineas]

    @staticmethod
    def crear_ejemplo(nombre_archivo):
        """Crea un archivo de texto de ejemplo para probar el programa."""
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(LeerArchivo.CONTENIDO_EJEMPLO)


class VentanaPrincipal:
    """Interfaz grafica del ejercicio 6.8."""

    def __init__(self):
        self.nombre_archivo = widgets.Text(
            value="prueba.txt", description="Archivo:",
            style={"description_width": "70px"}, layout=widgets.Layout(width="380px"))
        self.mayusculas = widgets.Checkbox(value=False, indent=False,
                                           description="Mostrar en mayúsculas")
        self.leer = widgets.Button(description="Leer archivo", button_style="success",
                                   layout=widgets.Layout(width="130px"))
        self.crear = widgets.Button(description="Crear prueba.txt de ejemplo",
                                    button_style="info",
                                    layout=widgets.Layout(width="230px"))
        self.limpiar = widgets.Button(description="Limpiar", button_style="danger",
                                      layout=widgets.Layout(width="100px"))
        self.alerta = widgets.HTML("")
        self.contenido = widgets.HTML("")

        for boton in (self.leer, self.crear, self.limpiar):
            boton.on_click(self.action_performed)

        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Lectura de archivos</h3>"),
             self.nombre_archivo, self.mayusculas,
             widgets.HBox([self.leer, self.crear, self.limpiar]),
             self.alerta,
             widgets.HTML("<b>Contenido del archivo:</b>"),
             self.contenido],
            layout=widgets.Layout(width="520px", border="1px solid #888",
                                  padding="12px"))

    def _mostrar(self, lineas):
        texto = "\n".join(lineas) if lineas else "(archivo vacío)"
        self.contenido.value = (
            "<pre style='background:#f4f4f4;border:1px solid #ccc;"
            "border-radius:4px;padding:8px;margin:4px 0'>"
            f"{html.escape(texto)}</pre>")

    def action_performed(self, evento):
        if evento is self.leer:
            self.alerta.value = ""
            self.contenido.value = ""
            nombre = self.nombre_archivo.value.strip()
            if nombre == "":
                self.alerta.value = html_alerta("Escriba el nombre del archivo.")
                return
            try:
                lineas = LeerArchivo.leer(nombre)
            except (OSError, UnicodeDecodeError):
                self.alerta.value = html_alerta("No se pudo leer el archivo.")
                return
            if self.mayusculas.value:
                lineas = LeerArchivo.a_mayusculas(lineas)
            self._mostrar(lineas)

        if evento is self.crear:
            self.alerta.value = ""
            nombre = self.nombre_archivo.value.strip() or "prueba.txt"
            try:
                LeerArchivo.crear_ejemplo(nombre)
            except OSError:
                self.alerta.value = html_alerta("No se pudo crear el archivo.")
                return
            self.nombre_archivo.value = nombre
            self.contenido.value = (
                "<i>Archivo de ejemplo creado. Pulse «Leer archivo».</i>")

        if evento is self.limpiar:
            self.alerta.value = ""
            self.contenido.value = ""


class Principal:
    """Punto de ingreso al programa (equivale al metodo main)."""

    @staticmethod
    def main():
        mi_ventana_principal = VentanaPrincipal()
        display(mi_ventana_principal.contenedor)
        return mi_ventana_principal


mi_ventana = Principal.main()


def probar_modelo():
    import os
    import tempfile
    ruta = os.path.join(tempfile.gettempdir(), "prueba_modelo_6_8.txt")
    LeerArchivo.crear_ejemplo(ruta)
    lineas = LeerArchivo.leer(ruta)
    assert lineas == ["Programación Orientada a Objetos",
                      "Universidad Nacional de Colombia",
                      "Ejercicio 6.8: lectura de archivos"]
    assert LeerArchivo.a_mayusculas(lineas)[0] == "PROGRAMACIÓN ORIENTADA A OBJETOS"
    os.remove(ruta)
    try:
        LeerArchivo.leer(ruta)
        raise AssertionError("debió lanzar OSError")
    except OSError:
        pass
    print("OK  Modelo: crear, leer línea a línea, mayúsculas y archivo inexistente")


def probar_interfaz():
    import os
    import tempfile
    ruta = os.path.join(tempfile.gettempdir(), "prueba_interfaz_6_8.txt")
    v = VentanaPrincipal()
    v.nombre_archivo.value = ruta

    v.crear.click()
    assert os.path.exists(ruta)
    v.leer.click()
    assert "Universidad Nacional de Colombia" in v.contenido.value
    assert v.alerta.value == ""

    v.mayusculas.value = True
    v.leer.click()
    assert "UNIVERSIDAD NACIONAL DE COLOMBIA" in v.contenido.value

    v.nombre_archivo.value = "no_existe_123.txt"
    v.leer.click()
    assert "No se pudo leer el archivo." in v.alerta.value and v.contenido.value == ""

    v.nombre_archivo.value = ""
    v.leer.click()
    assert "Escriba el nombre" in v.alerta.value

    v.limpiar.click()
    assert v.alerta.value == "" and v.contenido.value == ""
    os.remove(ruta)
    print("OK  Interfaz: crear, leer, mayúsculas, archivo inexistente y limpiar")


probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")
