import html
import math
import os
from enum import Enum

import ipywidgets as widgets
from IPython.display import display


# ----------------------------------------------------------------------
#  Datos enumerados
# ----------------------------------------------------------------------
class TipoCargo(Enum):
    """Tipo de cargo que tiene un empleado."""
    DIRECTIVO = "Directivo"
    ESTRATEGICO = "Estratégico"
    OPERATIVO = "Operativo"


class TipoGenero(Enum):
    """Genero de un empleado."""
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


# ----------------------------------------------------------------------
#  Modelo
# ----------------------------------------------------------------------
class Empleado:
    """Empleado de una empresa: nombre, apellidos, cargo, genero, salario
    por dia, dias trabajados, otros ingresos, pagos por salud y aporte
    a pensiones."""

    def __init__(self, nombre, apellidos, cargo, genero, salario_dia,
                 dias_trabajados, otros_ingresos, pagos_salud,
                 aporte_pensiones):
        if nombre.strip() == "" or apellidos.strip() == "":
            raise ValueError("El nombre y los apellidos son obligatorios.")
        if dias_trabajados < 1 or dias_trabajados > 31:
            raise ValueError("Los días trabajados deben estar entre 1 y 31.")
        if min(salario_dia, otros_ingresos, pagos_salud, aporte_pensiones) < 0:
            raise ValueError("Los valores monetarios no pueden ser negativos.")
        self.nombre = nombre.strip()
        self.apellidos = apellidos.strip()
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

    def calcular_nomina(self):
        """Salario mensual = (dias * sueldo por dia) + otros ingresos
        - pagos por salud - aporte pensiones."""
        return ((self.salario_dia * self.dias_trabajados)
                + self.otros_ingresos - self.pagos_salud
                - self.aporte_pensiones)


class ListaEmpleados:
    """Lista de empleados de la empresa."""

    def __init__(self):
        self.lista = []

    def agregar_empleado(self, empleado):
        self.lista.append(empleado)

    def calcular_total_nomina(self):
        """Suma los salarios mensuales de todos los empleados."""
        total = 0.0
        for empleado in self.lista:
            total += empleado.calcular_nomina()
        return total

    def obtener_matriz(self):
        """Convierte la lista en filas [nombre, apellidos, sueldo]
        (las usa la tabla de la ventana de nomina)."""
        return [[e.nombre, e.apellidos, f"{e.calcular_nomina():,.2f}"]
                for e in self.lista]

    def convertir_texto(self):
        """Convierte los datos de la lista a texto (para el archivo)."""
        texto = ""
        for e in self.lista:
            texto += (f"Nombre = {e.nombre}\n"
                      f"Apellidos = {e.apellidos}\n"
                      f"Cargo = {e.cargo.value}\n"
                      f"Género = {e.genero.value}\n"
                      f"Salario por día = ${e.salario_dia:,.2f}\n"
                      f"Días trabajados = {e.dias_trabajados}\n"
                      f"Otros ingresos = ${e.otros_ingresos:,.2f}\n"
                      f"Pagos salud = ${e.pagos_salud:,.2f}\n"
                      f"Aportes pensiones = ${e.aporte_pensiones:,.2f}\n"
                      f"Sueldo mensual = ${e.calcular_nomina():,.2f}\n"
                      "---------\n")
        texto += f"Total nómina = ${self.calcular_total_nomina():,.2f}\n"
        return texto


# ----------------------------------------------------------------------
#  Cuadros de dialogo (equivalen a JOptionPane)
# ----------------------------------------------------------------------
class Dialogos:
    """Cuadros de dialogo de mensaje (informacion, advertencia, error) y de
    confirmacion (Si / No). Se muestran dentro de la propia interfaz."""

    ESTILOS = {
        "informacion": ("#e8f1fb", "#0d47a1", "#64a0e6", "&#8505;"),
        "advertencia": ("#fff8e1", "#8a6100", "#f0b429", "&#9888;"),
        "error": ("#fdecea", "#b71c1c", "#f44336", "&#10006;"),
        "pregunta": ("#f3e5f5", "#4a148c", "#ab47bc", "&#63;"),
    }

    def __init__(self):
        self._al_confirmar = None
        self.mensaje = widgets.HTML("")
        self.si = widgets.Button(description="Sí", button_style="success",
                                 layout=widgets.Layout(width="80px"))
        self.no = widgets.Button(description="No", button_style="danger",
                                 layout=widgets.Layout(width="80px"))
        self.botones = widgets.HBox([self.si, self.no],
                                    layout=widgets.Layout(display="none"))
        self.si.on_click(self.action_performed)
        self.no.on_click(self.action_performed)
        self.contenedor = widgets.VBox([self.mensaje, self.botones])

    def _pintar(self, texto, tipo):
        fondo, color, borde, icono = Dialogos.ESTILOS[tipo]
        self.mensaje.value = (
            f"<div style='background:{fondo};color:{color};"
            f"border:1px solid {borde};border-radius:4px;padding:8px;"
            f"margin:6px 0'>{icono} {html.escape(texto)}</div>")

    def mostrar_mensaje(self, texto, tipo="informacion"):
        """Equivale a JOptionPane.showMessageDialog."""
        self._al_confirmar = None
        self.botones.layout.display = "none"
        self._pintar(texto, tipo)

    def confirmar(self, texto, al_confirmar):
        """Equivale a JOptionPane.showConfirmDialog (Si / No)."""
        self._al_confirmar = al_confirmar
        self._pintar(texto, "pregunta")
        self.botones.layout.display = "flex"

    def ocultar(self):
        self._al_confirmar = None
        self.mensaje.value = ""
        self.botones.layout.display = "none"

    def action_performed(self, evento):
        accion = self._al_confirmar
        if evento is self.si:
            self.ocultar()
            if accion is not None:
                accion()
        if evento is self.no:
            self.ocultar()


# ----------------------------------------------------------------------
#  Ventanas
# ----------------------------------------------------------------------
class VentanaAgregarEmpleado:
    """Ventana para ingresar los datos de un empleado."""

    def __init__(self, lista, dialogos):
        self.lista = lista
        self.dialogos = dialogos
        estilo = {"description_width": "150px"}
        caja = widgets.Layout(width="400px")

        self.nombre = widgets.Text(description="Nombre:", style=estilo, layout=caja)
        self.apellidos = widgets.Text(description="Apellidos:", style=estilo, layout=caja)
        self.cargo = widgets.Dropdown(
            options=[(c.value, c) for c in TipoCargo],
            description="Cargo:", style=estilo, layout=caja)
        self.genero = widgets.RadioButtons(
            options=[(g.value, g) for g in TipoGenero],
            description="Género:", style=estilo)
        self.salario_dia = widgets.Text(description="Salario por día:", style=estilo, layout=caja)
        self.dias = widgets.BoundedIntText(value=30, min=1, max=31,
                                           description="Días trabajados:",
                                           style=estilo, layout=caja)
        self.otros_ingresos = widgets.Text(description="Otros ingresos:", style=estilo, layout=caja)
        self.pagos_salud = widgets.Text(description="Pagos por salud:", style=estilo, layout=caja)
        self.pensiones = widgets.Text(description="Aportes pensiones:", style=estilo, layout=caja)
        self.agregar = widgets.Button(description="Agregar", button_style="success",
                                      layout=widgets.Layout(width="110px"))
        self.limpiar = widgets.Button(description="Borrar", button_style="danger",
                                      layout=widgets.Layout(width="110px"))
        self.agregar.on_click(self.action_performed)
        self.limpiar.on_click(self.action_performed)

        self.contenedor = widgets.VBox(
            [widgets.HTML("<h4 style='margin:0'>Agregar empleado</h4>"),
             self.nombre, self.apellidos, self.cargo, self.genero,
             self.salario_dia, self.dias, self.otros_ingresos,
             self.pagos_salud, self.pensiones,
             widgets.HBox([self.agregar, self.limpiar])])

    @staticmethod
    def _leer_numero(texto, etiqueta):
        """Convierte el texto a numero; lanza ValueError si no es numerico."""
        try:
            valor = float(texto.strip().replace(",", "."))
        except ValueError:
            raise ValueError(f"{etiqueta}: ingrese un valor numérico.") from None
        if not math.isfinite(valor):
            raise ValueError(f"{etiqueta}: ingrese un valor numérico.")
        return valor

    def _crear_empleado(self):
        """Lee los campos y crea el empleado. Lanza ValueError si hay error."""
        salario = self._leer_numero(self.salario_dia.value, "Salario por día")
        otros = self._leer_numero(self.otros_ingresos.value, "Otros ingresos")
        salud = self._leer_numero(self.pagos_salud.value, "Pagos por salud")
        pension = self._leer_numero(self.pensiones.value, "Aportes pensiones")
        return Empleado(self.nombre.value, self.apellidos.value,
                        self.cargo.value, self.genero.value, salario,
                        self.dias.value, otros, salud, pension)

    def limpiar_campos(self):
        for campo in (self.nombre, self.apellidos, self.salario_dia,
                      self.otros_ingresos, self.pagos_salud, self.pensiones):
            campo.value = ""
        self.dias.value = 30

    def action_performed(self, evento):
        if evento is self.agregar:
            try:
                empleado = self._crear_empleado()
            except ValueError as error:
                self.dialogos.mostrar_mensaje(str(error), "error")
                return
            self.lista.agregar_empleado(empleado)
            self.dialogos.mostrar_mensaje("El empleado ha sido agregado.", "informacion")
            self.limpiar_campos()
        if evento is self.limpiar:
            self.limpiar_campos()
            self.dialogos.ocultar()


class VentanaNomina:
    """Ventana que muestra en una tabla los empleados y el total de la nomina."""

    def __init__(self, lista):
        self.lista = lista
        self.tabla = widgets.HTML("")
        self.total = widgets.HTML("")
        self.contenedor = widgets.VBox(
            [widgets.HTML("<h4 style='margin:0'>Nómina de empleados</h4>"),
             self.tabla, self.total])
        self.actualizar()

    def actualizar(self):
        filas = "".join(
            "<tr>" + "".join(
                f"<td style='border:1px solid #bbb;padding:4px 8px"
                f"{';text-align:right' if i == 2 else ''}'>{html.escape(c)}</td>"
                for i, c in enumerate(fila)) + "</tr>"
            for fila in self.lista.obtener_matriz())
        if filas == "":
            filas = ("<tr><td colspan='3' style='padding:6px'>"
                     "<i>(no hay empleados)</i></td></tr>")
        self.tabla.value = (
            "<table style='border-collapse:collapse'>"
            "<tr style='background:#e0e0e0'>"
            "<th style='border:1px solid #bbb;padding:4px 8px'>NOMBRE</th>"
            "<th style='border:1px solid #bbb;padding:4px 8px'>APELLIDOS</th>"
            "<th style='border:1px solid #bbb;padding:4px 8px'>SUELDO</th></tr>"
            f"{filas}</table>")
        self.total.value = ("<p><b>Total nómina mensual = $ "
                            f"{self.lista.calcular_total_nomina():,.2f}</b></p>")


class VentanaGuardarArchivo:
    """Ventana que pide una carpeta y genera el archivo Nómina.txt
    (equivale al JFileChooser de directorios)."""
    NOMBRE_ARCHIVO = "Nómina.txt"

    def __init__(self, lista, dialogos):
        self.lista = lista
        self.dialogos = dialogos
        self.carpeta = widgets.Text(value=".", description="Carpeta:",
                                    style={"description_width": "70px"},
                                    layout=widgets.Layout(width="420px"))
        self.guardar = widgets.Button(description="Guardar", button_style="success",
                                      layout=widgets.Layout(width="110px"))
        self.guardar.on_click(self.action_performed)
        self.contenedor = widgets.VBox(
            [widgets.HTML("<h4 style='margin:0'>Guardar archivo</h4>"),
             widgets.HTML("Escriba la carpeta donde se generará "
                          f"<code>{self.NOMBRE_ARCHIVO}</code> "
                          "(<code>.</code> = carpeta actual)."),
             self.carpeta, self.guardar])

    def _escribir(self, ruta):
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(self.lista.convertir_texto())
        except OSError:
            self.dialogos.mostrar_mensaje("No se pudo escribir el archivo.", "error")
            return
        self.dialogos.mostrar_mensaje(
            f"El archivo de la nómina {self.NOMBRE_ARCHIVO} se ha creado en "
            f"{os.path.dirname(ruta) or '.'}", "informacion")

    def action_performed(self, evento):
        if evento is self.guardar:
            if len(self.lista.lista) == 0:
                self.dialogos.mostrar_mensaje(
                    "No hay empleados para guardar.", "advertencia")
                return
            carpeta = self.carpeta.value.strip()
            if not os.path.isdir(carpeta):
                self.dialogos.mostrar_mensaje("La carpeta no existe.", "error")
                return
            ruta = os.path.join(carpeta, self.NOMBRE_ARCHIVO)
            if os.path.exists(ruta):
                self.dialogos.confirmar(
                    "El archivo ya existe. ¿Desea reemplazarlo?",
                    lambda: self._escribir(ruta))
            else:
                self._escribir(ruta)


class VentanaPrincipal:
    """Ventana principal con la barra de menu del ejercicio 8.4."""

    def __init__(self):
        self.empleados = ListaEmpleados()
        self.dialogos = Dialogos()
        self.ventana_actual = None

        self.item_menu1 = widgets.Button(description="Agregar empleado",
                                         icon="user-plus",
                                         layout=widgets.Layout(width="170px"))
        self.item_menu2 = widgets.Button(description="Calcular nómina",
                                         icon="calculator",
                                         layout=widgets.Layout(width="170px"))
        self.item_menu3 = widgets.Button(description="Guardar archivo",
                                         icon="save",
                                         layout=widgets.Layout(width="170px"))
        for item in (self.item_menu1, self.item_menu2, self.item_menu3):
            item.on_click(self.action_performed)

        self.barra_menu = widgets.HBox(
            [widgets.HTML("<b>Menú:</b>&nbsp;"), self.item_menu1,
             self.item_menu2, self.item_menu3])
        self.area = widgets.VBox([widgets.HTML("<i>Seleccione una opción del menú.</i>")])
        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Nómina</h3>"),
             self.barra_menu, self.area, self.dialogos.contenedor],
            layout=widgets.Layout(width="620px", border="1px solid #888",
                                  padding="12px"))

    def _mostrar(self, ventana):
        self.dialogos.ocultar()
        if hasattr(ventana, "actualizar"):
            ventana.actualizar()
        self.ventana_actual = ventana
        self.area.children = [ventana.contenedor]

    def action_performed(self, evento):
        if evento is self.item_menu1:
            self._mostrar(VentanaAgregarEmpleado(self.empleados, self.dialogos))
        if evento is self.item_menu2:
            self._mostrar(VentanaNomina(self.empleados))
        if evento is self.item_menu3:
            self._mostrar(VentanaGuardarArchivo(self.empleados, self.dialogos))


class Principal:
    """Punto de ingreso al programa (equivale al metodo main)."""

    @staticmethod
    def main():
        mi_ventana_principal = VentanaPrincipal()
        display(mi_ventana_principal.contenedor)
        return mi_ventana_principal


mi_ventana = Principal.main()


# ----------------------------------------------------------------------
#  Pruebas automaticas
# ----------------------------------------------------------------------
def probar_modelo():
    e = Empleado("Ana", "Ruiz", TipoCargo.OPERATIVO, TipoGenero.FEMENINO,
                 50000, 30, 100000, 60000, 60000)
    assert e.calcular_nomina() == 1480000
    lista = ListaEmpleados()
    lista.agregar_empleado(e)
    lista.agregar_empleado(Empleado("Luis", "Soto", TipoCargo.DIRECTIVO,
                                    TipoGenero.MASCULINO, 100000, 20, 0, 0, 0))
    assert lista.calcular_total_nomina() == 1480000 + 2000000
    assert lista.calcular_total_nomina() == 3480000      # no se acumula
    assert lista.obtener_matriz()[0] == ["Ana", "Ruiz", "1,480,000.00"]
    assert "Total nómina = $3,480,000.00" in lista.convertir_texto()
    for datos in [("", "x", 30, 0), ("a", "b", 0, 0), ("a", "b", 32, 0),
                  ("a", "b", 30, -1)]:
        try:
            Empleado(datos[0], datos[1], TipoCargo.OPERATIVO,
                     TipoGenero.MASCULINO, 1000, datos[2], datos[3], 0, 0)
            raise AssertionError("debió lanzar ValueError")
        except ValueError:
            pass
    print("OK  Modelo: cálculo de nómina, total, matriz, texto y validaciones")


def probar_interfaz():
    import tempfile
    v = VentanaPrincipal()

    v.item_menu1.click()
    a = v.ventana_actual
    a.nombre.value, a.apellidos.value = "Ana", "Ruiz"
    a.cargo.value = TipoCargo.ESTRATEGICO
    a.genero.value = TipoGenero.FEMENINO
    a.salario_dia.value, a.dias.value = "50000", 30
    a.otros_ingresos.value, a.pagos_salud.value, a.pensiones.value = "100000", "60000", "60000"
    a.agregar.click()
    assert len(v.empleados.lista) == 1
    assert "ha sido agregado" in v.dialogos.mensaje.value and a.nombre.value == ""

    a.nombre.value, a.apellidos.value = "Luis", "Soto"
    a.salario_dia.value = "abc"
    a.agregar.click()
    assert len(v.empleados.lista) == 1 and "valor numérico" in v.dialogos.mensaje.value

    a.salario_dia.value, a.otros_ingresos.value = "80000,50", "0"
    a.pagos_salud.value, a.pensiones.value = "0", "0"
    a.agregar.click()
    assert len(v.empleados.lista) == 2

    v.item_menu2.click()
    assert "1,480,000.00" in v.ventana_actual.tabla.value
    esperado = f"{v.empleados.calcular_total_nomina():,.2f}"
    assert esperado in v.ventana_actual.total.value

    v.item_menu3.click()
    g = v.ventana_actual
    carpeta = tempfile.mkdtemp()
    g.carpeta.value = carpeta + "_no_existe"
    g.guardar.click()
    assert "no existe" in v.dialogos.mensaje.value
    g.carpeta.value = carpeta
    g.guardar.click()
    ruta = os.path.join(carpeta, "Nómina.txt")
    assert os.path.exists(ruta) and "se ha creado" in v.dialogos.mensaje.value
    with open(ruta, encoding="utf-8") as f:
        assert "Total nómina" in f.read()
    g.guardar.click()
    assert v.dialogos.botones.layout.display == "flex"
    v.dialogos.no.click()
    assert v.dialogos.botones.layout.display == "none"
    g.guardar.click()
    v.dialogos.si.click()
    assert "se ha creado" in v.dialogos.mensaje.value
    os.remove(ruta)

    vacia = VentanaPrincipal()
    vacia.item_menu3.click()
    vacia.ventana_actual.guardar.click()
    assert "No hay empleados" in vacia.dialogos.mensaje.value
    print("OK  Interfaz: agregar, errores, tabla, total, guardar y confirmación")


probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")

