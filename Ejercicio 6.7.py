import html
import ipywidgets as widgets
from IPython.display import display


def html_alerta(mensaje):
    return ("<div style='background:#fdecea;color:#b71c1c;border:1px solid #f44336;"
            "border-radius:4px;padding:6px;margin:6px 0'>&#9888; "
            f"{html.escape(mensaje)}</div>")


class EquipoLlenoError(Exception):
    """Se lanza al intentar anadir un programador a un equipo completo."""


class Programador:
    """Integrante de un equipo: nombre y apellidos."""

    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos


class EquipoMaratonProgramacion:
    """Equipo de programadores (minimo 2, maximo 3) de una maraton."""
    MINIMO = 2
    MAXIMO = 3
    LONGITUD_MAXIMA = 20

    def __init__(self, nombre_equipo, universidad, lenguaje_programacion):
        self.nombre_equipo = nombre_equipo
        self.universidad = universidad
        self.lenguaje_programacion = lenguaje_programacion
        self.programadores = []

    @property
    def tamano_equipo(self):
        return len(self.programadores)

    def esta_lleno(self):
        """True si el equipo ya tiene el maximo de programadores."""
        return self.tamano_equipo == EquipoMaratonProgramacion.MAXIMO

    def tiene_minimo(self):
        """True si el equipo ya tiene los programadores minimos para competir."""
        return self.tamano_equipo >= EquipoMaratonProgramacion.MINIMO

    def anadir(self, programador):
        """Anade un programador; si el equipo esta lleno lanza la excepcion."""
        if self.esta_lleno():
            raise EquipoLlenoError("El equipo está completo. "
                                   "No se pudo agregar programador.")
        self.programadores.append(programador)

    @staticmethod
    def validar_campo(campo, etiqueta="campo"):
        """Valida que el campo sea solo texto y de menos de 20 caracteres."""
        if campo.strip() == "":
            raise ValueError(f"El {etiqueta} es obligatorio.")
        for c in campo:
            if c.isdigit():
                raise ValueError(f"El {etiqueta} no puede tener dígitos.")
        if len(campo) >= EquipoMaratonProgramacion.LONGITUD_MAXIMA:
            raise ValueError(f"La longitud del {etiqueta} debe ser inferior "
                             "a 20 caracteres.")


class VentanaPrincipal:
    """Interfaz grafica del ejercicio 6.7."""

    def __init__(self):
        self.equipo = None
        estilo = {"description_width": "110px"}
        caja = widgets.Layout(width="320px")


        self.nombre_equipo = widgets.Text(description="Equipo:", style=estilo, layout=caja)
        self.universidad = widgets.Text(description="Universidad:", style=estilo, layout=caja)
        self.lenguaje = widgets.Text(description="Lenguaje:", style=estilo, layout=caja)
        self.crear_equipo = widgets.Button(description="Crear equipo", button_style="success",
                                           layout=widgets.Layout(width="130px"))

        self.nombre = widgets.Text(description="Nombre:", style=estilo, layout=caja,
                                   disabled=True)
        self.apellidos = widgets.Text(description="Apellidos:", style=estilo, layout=caja,
                                      disabled=True)
        self.anadir = widgets.Button(description="Añadir programador",
                                     button_style="primary", disabled=True,
                                     layout=widgets.Layout(width="170px"))
        self.reiniciar = widgets.Button(description="Reiniciar", button_style="danger",
                                        layout=widgets.Layout(width="110px"))
        self.alerta = widgets.HTML("")
        self.resumen = widgets.HTML("")

        for boton in (self.crear_equipo, self.anadir, self.reiniciar):
            boton.on_click(self.action_performed)

        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Equipo de maratón de programación</h3>"),
             widgets.HTML("<b>1. Datos del equipo</b>"),
             self.nombre_equipo, self.universidad, self.lenguaje, self.crear_equipo,
             widgets.HTML("<b>2. Integrantes (mínimo 2, máximo 3)</b>"),
             self.nombre, self.apellidos,
             widgets.HBox([self.anadir, self.reiniciar]),
             self.alerta, self.resumen],
            layout=widgets.Layout(width="420px", border="1px solid #888",
                                  padding="12px"))


    def _actualizar_resumen(self):
        e = self.equipo
        if e is None:
            self.resumen.value = ""
            return
        filas = "".join(
            f"<li>{html.escape(p.nombre)} {html.escape(p.apellidos)}</li>"
            for p in e.programadores) or "<li><i>(sin integrantes)</i></li>"
        estado = ("Equipo lleno" if e.esta_lleno() else
                  "Cumple el mínimo para competir" if e.tiene_minimo() else
                  "Faltan integrantes (mínimo 2)")
        self.resumen.value = (
            "<div style='background:#eef7ee;border:1px solid #8bc48b;"
            "border-radius:4px;padding:8px;margin:6px 0'>"
            f"<b>{html.escape(e.nombre_equipo)}</b> — {html.escape(e.universidad)} "
            f"— {html.escape(e.lenguaje_programacion)}<br>"
            f"Integrantes: {e.tamano_equipo}/{EquipoMaratonProgramacion.MAXIMO} "
            f"({estado})<ul style='margin:4px 0'>{filas}</ul></div>")

    def _habilitar_integrantes(self, habilitar):
        self.nombre.disabled = not habilitar
        self.apellidos.disabled = not habilitar
        self.anadir.disabled = not habilitar


    def action_performed(self, evento):
        if evento is self.crear_equipo:
            self.alerta.value = ""
            try:
                EquipoMaratonProgramacion.validar_campo(
                    self.nombre_equipo.value, "nombre del equipo")
                EquipoMaratonProgramacion.validar_campo(
                    self.universidad.value, "nombre de la universidad")
                EquipoMaratonProgramacion.validar_campo(
                    self.lenguaje.value, "lenguaje de programación")
            except ValueError as error:
                self.alerta.value = html_alerta(str(error))
                return
            self.equipo = EquipoMaratonProgramacion(
                self.nombre_equipo.value.strip(), self.universidad.value.strip(),
                self.lenguaje.value.strip())
            self._habilitar_integrantes(True)
            self._actualizar_resumen()

        if evento is self.anadir:
            self.alerta.value = ""
            try:
                EquipoMaratonProgramacion.validar_campo(self.nombre.value, "nombre")
                EquipoMaratonProgramacion.validar_campo(self.apellidos.value, "apellido")
                self.equipo.anadir(Programador(self.nombre.value.strip(),
                                               self.apellidos.value.strip()))
            except (ValueError, EquipoLlenoError) as error:
                self.alerta.value = html_alerta(str(error))
                return
            self.nombre.value = ""
            self.apellidos.value = ""
            self._actualizar_resumen()

        if evento is self.reiniciar:
            for campo in (self.nombre_equipo, self.universidad, self.lenguaje,
                          self.nombre, self.apellidos):
                campo.value = ""
            self.equipo = None
            self._habilitar_integrantes(False)
            self.alerta.value = ""
            self._actualizar_resumen()


class Principal:
    """Punto de ingreso al programa (equivale al metodo main)."""

    @staticmethod
    def main():
        mi_ventana_principal = VentanaPrincipal()
        display(mi_ventana_principal.contenedor)
        return mi_ventana_principal


mi_ventana = Principal.main()


def probar_modelo():
    e = EquipoMaratonProgramacion("EquipoUNAL", "Nacional", "Java")
    assert e.tamano_equipo == 0 and not e.esta_lleno() and not e.tiene_minimo()
    e.anadir(Programador("Pedro", "Pérez"))
    e.anadir(Programador("Diana", "Soto"))
    assert e.tiene_minimo() and not e.esta_lleno()
    e.anadir(Programador("Luis", "Gómez"))
    assert e.esta_lleno()
    try:
        e.anadir(Programador("Ana", "Ruiz"))
        raise AssertionError("debió lanzar EquipoLlenoError")
    except EquipoLlenoError as error:
        assert "equipo está completo" in str(error)
    EquipoMaratonProgramacion.validar_campo("Pedro")
    for texto, parte in [("Pablo3", "dígitos"), ("a" * 20, "inferior a 20"),
                         ("   ", "obligatorio")]:
        try:
            EquipoMaratonProgramacion.validar_campo(texto, "nombre")
            raise AssertionError("debió lanzar ValueError")
        except ValueError as error:
            assert parte in str(error), (texto, str(error))
    EquipoMaratonProgramacion.validar_campo("a" * 19)
    print("OK  Modelo: añadir, equipo lleno y validación de campos")


def probar_interfaz():
    v = VentanaPrincipal()
    assert v.anadir.disabled
    v.nombre_equipo.value = "EquipoUNAL"
    v.universidad.value = "Nacional"
    v.lenguaje.value = "Java"
    v.crear_equipo.click()
    assert v.equipo is not None and not v.anadir.disabled and v.alerta.value == ""

    v.nombre.value, v.apellidos.value = "Pablo3", "Pérez"
    v.anadir.click()
    assert "no puede tener dígitos" in v.alerta.value and v.equipo.tamano_equipo == 0

    for n, a in [("Pedro", "Pérez"), ("Diana", "Soto"), ("Luis", "Gómez")]:
        v.nombre.value, v.apellidos.value = n, a
        v.anadir.click()
        assert v.alerta.value == ""
    assert v.equipo.esta_lleno() and "3/3" in v.resumen.value

    v.nombre.value, v.apellidos.value = "Ana", "Ruiz"
    v.anadir.click()
    assert "equipo está completo" in v.alerta.value

    v.reiniciar.click()
    assert v.equipo is None and v.anadir.disabled and v.resumen.value == ""

    v.crear_equipo.click()
    assert "obligatorio" in v.alerta.value and v.equipo is None
    print("OK  Interfaz: crear equipo, errores, equipo lleno y reiniciar")


probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")
