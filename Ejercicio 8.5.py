import html
import re
from datetime import date, datetime

import ipywidgets as widgets
from IPython.display import display


# ----------------------------------------------------------------------
#  Utilidades
# ----------------------------------------------------------------------
def convertir_fecha(texto):
    """Convierte un texto con formato aaaa-mm-dd a datetime.date.
    Lanza ValueError si el formato o la fecha no son validos."""
    texto = texto.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", texto) is None:
        raise ValueError("La fecha debe tener el formato aaaa-mm-dd.")
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("La fecha ingresada no existe en el calendario.") from None


def pesos(valor):
    return f"${valor:,.0f}"


# ----------------------------------------------------------------------
#  Modelo
# ----------------------------------------------------------------------
class Huesped:
    """Persona que se aloja en el hotel."""

    def __init__(self, nombre, apellidos, documento):
        nombre, apellidos, documento = nombre.strip(), apellidos.strip(), documento.strip()
        if nombre == "" or apellidos == "" or documento == "":
            raise ValueError("El nombre, los apellidos y el documento son obligatorios.")
        if not (documento.isascii() and documento.isdigit()):
            raise ValueError("El documento debe contener solo números.")
        self.nombre = nombre
        self.apellidos = apellidos
        self.documento = documento

    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"


class Habitacion:
    """Habitacion simple del hotel."""

    def __init__(self, numero, precio_dia):
        self.numero = numero
        self.precio_dia = precio_dia
        self.huesped = None
        self.fecha_ingreso = None

    def esta_ocupada(self):
        return self.huesped is not None

    def ocupar(self, huesped, fecha_ingreso):
        if self.esta_ocupada():
            raise ValueError(f"La habitación {self.numero} ya está ocupada.")
        self.huesped = huesped
        self.fecha_ingreso = fecha_ingreso

    def liberar(self):
        self.huesped = None
        self.fecha_ingreso = None


class Hotel:
    """Hotel con 10 habitaciones simples: de la 1 a la 5 cuestan $120.000
    por dia y de la 6 a la 10 cuestan $160.000 por dia."""
    NUM_HABITACIONES = 10

    def __init__(self):
        self.habitaciones = []
        for numero in range(1, Hotel.NUM_HABITACIONES + 1):
            precio = 120000 if numero <= 5 else 160000
            self.habitaciones.append(Habitacion(numero, precio))

    def obtener_habitacion(self, numero):
        """Devuelve la habitacion; lanza ValueError si el numero no es valido."""
        if not isinstance(numero, int) or not 1 <= numero <= Hotel.NUM_HABITACIONES:
            raise ValueError(
                f"El número de habitación debe estar entre 1 y {Hotel.NUM_HABITACIONES}.")
        return self.habitaciones[numero - 1]

    def ingresar_huesped(self, numero, huesped, fecha_ingreso):
        self.obtener_habitacion(numero).ocupar(huesped, fecha_ingreso)

    def obtener_ocupada(self, numero):
        """Devuelve la habitacion si esta ocupada; si no, lanza ValueError."""
        habitacion = self.obtener_habitacion(numero)
        if not habitacion.esta_ocupada():
            raise ValueError(f"La habitación {numero} no está ocupada.")
        return habitacion

    def calcular_estadia(self, numero, fecha_salida):
        """Devuelve (dias, total a pagar). La fecha de salida debe ser
        posterior a la de ingreso."""
        habitacion = self.obtener_ocupada(numero)
        dias = (fecha_salida - habitacion.fecha_ingreso).days
        if dias <= 0:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de ingreso.")
        return dias, dias * habitacion.precio_dia

    def registrar_salida(self, numero, fecha_salida):
        """Calcula la estadia y deja la habitacion libre."""
        dias, total = self.calcular_estadia(numero, fecha_salida)
        self.obtener_habitacion(numero).liberar()
        return dias, total

    def contar_ocupadas(self):
        return sum(1 for h in self.habitaciones if h.esta_ocupada())


# ----------------------------------------------------------------------
#  Cuadros de dialogo (equivalen a JOptionPane)
# ----------------------------------------------------------------------
class Dialogos:
    """Cuadros de dialogo de mensaje (informacion, advertencia, error).
    Se muestran dentro de la propia interfaz."""

    ESTILOS = {
        "informacion": ("#e8f1fb", "#0d47a1", "#64a0e6", "&#8505;"),
        "advertencia": ("#fff8e1", "#8a6100", "#f0b429", "&#9888;"),
        "error": ("#fdecea", "#b71c1c", "#f44336", "&#10006;"),
    }

    def __init__(self):
        self.mensaje = widgets.HTML("")
        self.contenedor = widgets.VBox([self.mensaje])

    def mostrar_mensaje(self, texto, tipo="informacion"):
        """Equivale a JOptionPane.showMessageDialog."""
        fondo, color, borde, icono = Dialogos.ESTILOS[tipo]
        self.mensaje.value = (
            f"<div style='background:{fondo};color:{color};"
            f"border:1px solid {borde};border-radius:4px;padding:8px;"
            f"margin:6px 0'>{icono} {html.escape(texto)}</div>")

    def ocultar(self):
        self.mensaje.value = ""


# ----------------------------------------------------------------------
#  Ventanas
# ----------------------------------------------------------------------
class VentanaHabitaciones:
    """Muestra las 10 habitaciones en una cuadricula (2 filas x 5 columnas).
    Verde = libre, rojo = ocupada. Al pulsar una habitacion libre se abre la
    ventana de ingreso."""

    def __init__(self, hotel, dialogos, al_elegir_libre):
        self.hotel = hotel
        self.dialogos = dialogos
        self.al_elegir_libre = al_elegir_libre
        self.botones = []
        self.celdas = []
        for habitacion in hotel.habitaciones:
            boton = widgets.Button(layout=widgets.Layout(width="100%"))
            boton.on_click(self.action_performed)
            detalle = widgets.HTML()
            self.botones.append(boton)
            self.celdas.append(widgets.VBox([boton, detalle],
                                            layout=widgets.Layout(align_items="center")))
        self.cuadricula = widgets.GridBox(
            self.celdas,
            layout=widgets.Layout(grid_template_columns="repeat(5, 1fr)",
                                  grid_gap="8px 10px", width="100%"))
        self.resumen = widgets.HTML()
        self.contenedor = widgets.VBox(
            [widgets.HTML("<h4 style='margin:0'>Consultar habitaciones</h4>"
                          "<small>Pulse una habitación libre (verde) para registrar "
                          "el ingreso de un huésped.</small>"),
             self.cuadricula, self.resumen])
        self.actualizar()

    def actualizar(self):
        for habitacion, boton, celda in zip(self.hotel.habitaciones,
                                            self.botones, self.celdas):
            if habitacion.esta_ocupada():
                boton.description = f"Hab. {habitacion.numero} - Ocupada"
                boton.button_style = "danger"
                texto = (f"{html.escape(habitacion.huesped.nombre_completo())}<br>"
                         f"Desde {habitacion.fecha_ingreso.isoformat()}")
            else:
                boton.description = f"Hab. {habitacion.numero} - Libre"
                boton.button_style = "success"
                texto = f"{pesos(habitacion.precio_dia)} / día"
            celda.children = [boton, widgets.HTML(
                f"<div style='text-align:center;font-size:12px'>{texto}</div>")]
        ocupadas = self.hotel.contar_ocupadas()
        libres = Hotel.NUM_HABITACIONES - ocupadas
        self.resumen.value = (f"<p><b>Libres:</b> {libres} &nbsp; "
                              f"<b>Ocupadas:</b> {ocupadas}</p>")

    def action_performed(self, evento):
        for habitacion, boton in zip(self.hotel.habitaciones, self.botones):
            if evento is boton:
                if habitacion.esta_ocupada():
                    self.dialogos.mostrar_mensaje(
                        f"La habitación {habitacion.numero} está ocupada.", "error")
                else:
                    self.al_elegir_libre(habitacion.numero)


class VentanaIngreso:
    """Ventana para registrar el ingreso de un huesped a una habitacion."""

    def __init__(self, hotel, numero, dialogos, al_registrar):
        self.hotel = hotel
        self.numero = numero
        self.dialogos = dialogos
        self.al_registrar = al_registrar
        habitacion = hotel.obtener_habitacion(numero)
        estilo = {"description_width": "120px"}
        caja = widgets.Layout(width="380px")

        self.fecha = widgets.Text(value=date.today().isoformat(),
                                  description="Fecha ingreso:", style=estilo, layout=caja,
                                  placeholder="aaaa-mm-dd")
        self.nombre = widgets.Text(description="Nombre:", style=estilo, layout=caja)
        self.apellidos = widgets.Text(description="Apellidos:", style=estilo, layout=caja)
        self.documento = widgets.Text(description="Documento:", style=estilo, layout=caja)
        self.registrar = widgets.Button(description="Registrar ingreso",
                                        button_style="success", icon="check",
                                        layout=widgets.Layout(width="160px"))
        self.cancelar = widgets.Button(description="Cancelar", button_style="danger",
                                       layout=widgets.Layout(width="110px"))
        self.registrar.on_click(self.action_performed)
        self.cancelar.on_click(self.action_performed)
        self.contenedor = widgets.VBox(
            [widgets.HTML(f"<h4 style='margin:0'>Ingreso a la habitación {numero}</h4>"
                          f"<small>Precio por día: {pesos(habitacion.precio_dia)}. "
                          "Todos los campos son obligatorios.</small>"),
             self.fecha, self.nombre, self.apellidos, self.documento,
             widgets.HBox([self.registrar, self.cancelar])])

    def action_performed(self, evento):
        if evento is self.registrar:
            try:
                fecha = convertir_fecha(self.fecha.value)
                huesped = Huesped(self.nombre.value, self.apellidos.value,
                                  self.documento.value)
                self.hotel.ingresar_huesped(self.numero, huesped, fecha)
            except ValueError as error:
                self.dialogos.mostrar_mensaje(str(error), "error")
                return
            self.al_registrar(
                f"Ingreso registrado: {huesped.nombre_completo()} en la "
                f"habitación {self.numero}.")
        if evento is self.cancelar:
            self.al_registrar(None)


class VentanaSalida:
    """Ventana para registrar la salida de un huesped: pide el numero de
    habitacion, la fecha de salida, calcula dias y total y libera la habitacion."""

    def __init__(self, hotel, dialogos, al_terminar=None):
        self.hotel = hotel
        self.dialogos = dialogos
        self.al_terminar = al_terminar
        self.numero_actual = None
        self.fecha_salida = None
        estilo = {"description_width": "130px"}
        caja = widgets.Layout(width="380px")

        self.numero = widgets.Text(description="Habitación No.:", style=estilo,
                                   layout=widgets.Layout(width="300px"))
        self.buscar = widgets.Button(description="Buscar", icon="search",
                                     layout=widgets.Layout(width="100px"))
        self.datos = widgets.HTML()
        self.fecha = widgets.Text(description="Fecha salida:", style=estilo, layout=caja,
                                  placeholder="aaaa-mm-dd", disabled=True)
        self.calcular = widgets.Button(description="Calcular", icon="calculator",
                                       disabled=True,
                                       layout=widgets.Layout(width="130px"))
        self.resultado = widgets.HTML()
        self.registrar = widgets.Button(description="Registrar salida",
                                        button_style="success", icon="sign-out",
                                        disabled=True,
                                        layout=widgets.Layout(width="160px"))
        for boton in (self.buscar, self.calcular, self.registrar):
            boton.on_click(self.action_performed)
        self.numero.observe(self._numero_cambio, names="value")
        self.fecha.observe(self._fecha_cambio, names="value")

        self.contenedor = widgets.VBox(
            [widgets.HTML("<h4 style='margin:0'>Salida de huéspedes</h4>"),
             widgets.HBox([self.numero, self.buscar]), self.datos, self.fecha,
             widgets.HBox([self.calcular, self.registrar]), self.resultado])

    # --- control de habilitacion de botones ---
    def _reiniciar_calculo(self):
        self.fecha_salida = None
        self.registrar.disabled = True
        self.resultado.value = ""

    def _numero_cambio(self, cambio):
        """Si se cambia el numero, hay que volver a buscar la habitacion."""
        self.numero_actual = None
        self.datos.value = ""
        self.fecha.disabled = True
        self.calcular.disabled = True
        self._reiniciar_calculo()

    def _fecha_cambio(self, cambio):
        """El boton Calcular se habilita solo si la fecha tiene formato valido."""
        self._reiniciar_calculo()
        try:
            convertir_fecha(self.fecha.value)
            self.calcular.disabled = self.numero_actual is None
        except ValueError:
            self.calcular.disabled = True

    # --- eventos ---
    def action_performed(self, evento):
        if evento is self.buscar:
            self._buscar()
        if evento is self.calcular:
            self._calcular()
        if evento is self.registrar:
            self._registrar()

    def _buscar(self):
        self.dialogos.ocultar()
        try:
            texto = self.numero.value.strip()
            if not (texto.isascii() and texto.isdigit()):
                raise ValueError("Ingrese un número de habitación válido.")
            habitacion = self.hotel.obtener_ocupada(int(texto))
        except ValueError as error:
            self.dialogos.mostrar_mensaje(str(error), "error")
            return
        self.numero_actual = habitacion.numero
        h = habitacion.huesped
        self.datos.value = (
            "<div style='border:1px solid #bbb;border-radius:4px;padding:6px;"
            "margin:6px 0'>"
            f"<b>Huésped:</b> {html.escape(h.nombre_completo())}<br>"
            f"<b>Documento:</b> {html.escape(h.documento)}<br>"
            f"<b>Fecha de ingreso:</b> {habitacion.fecha_ingreso.isoformat()}<br>"
            f"<b>Precio por día:</b> {pesos(habitacion.precio_dia)}</div>")
        self.fecha.disabled = False
        self._fecha_cambio(None)

    def _calcular(self):
        self.dialogos.ocultar()
        try:
            fecha = convertir_fecha(self.fecha.value)
            dias, total = self.hotel.calcular_estadia(self.numero_actual, fecha)
        except ValueError as error:
            self.resultado.value = ""
            self.registrar.disabled = True
            self.dialogos.mostrar_mensaje(str(error), "error")
            return
        self.fecha_salida = fecha
        self.resultado.value = (
            f"<p><b>Días de estadía:</b> {dias}<br>"
            f"<b>Total a pagar:</b> {pesos(total)}</p>")
        self.registrar.disabled = False

    def _registrar(self):
        if self.numero_actual is None or self.fecha_salida is None:
            return
        try:
            dias, total = self.hotel.registrar_salida(self.numero_actual,
                                                      self.fecha_salida)
        except ValueError as error:
            self.dialogos.mostrar_mensaje(str(error), "error")
            return
        numero = self.numero_actual
        self.numero.value = ""          # reinicia la ventana (observe)
        self.fecha.value = ""
        self.dialogos.mostrar_mensaje(
            f"Salida registrada. La habitación {numero} quedó libre. "
            f"Total cobrado: {pesos(total)} por {dias} día(s).", "informacion")
        if self.al_terminar is not None:
            self.al_terminar()


class VentanaPrincipal:
    """Ventana principal con la barra de menu del ejercicio 8.5."""

    def __init__(self):
        self.hotel = Hotel()
        self.dialogos = Dialogos()
        self.ventana_actual = None

        self.item_menu1 = widgets.Button(description="Consultar habitaciones",
                                         icon="bed",
                                         layout=widgets.Layout(width="200px"))
        self.item_menu2 = widgets.Button(description="Salida de huéspedes",
                                         icon="sign-out",
                                         layout=widgets.Layout(width="200px"))
        self.item_menu1.on_click(self.action_performed)
        self.item_menu2.on_click(self.action_performed)

        self.barra_menu = widgets.HBox(
            [widgets.HTML("<b>Menú:</b>&nbsp;"), self.item_menu1, self.item_menu2])
        self.area = widgets.VBox([widgets.HTML("<i>Seleccione una opción del menú.</i>")])
        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Hotel</h3>"),
             self.barra_menu, self.area, self.dialogos.contenedor],
            layout=widgets.Layout(width="700px", border="1px solid #888",
                                  padding="12px"))

    def _mostrar(self, ventana):
        self.ventana_actual = ventana
        self.area.children = [ventana.contenedor]

    def abrir_habitaciones(self, mensaje=None):
        self.dialogos.ocultar()
        self._mostrar(VentanaHabitaciones(self.hotel, self.dialogos,
                                          self.abrir_ingreso))
        if mensaje:
            self.dialogos.mostrar_mensaje(mensaje, "informacion")

    def abrir_ingreso(self, numero):
        self.dialogos.ocultar()
        self._mostrar(VentanaIngreso(self.hotel, numero, self.dialogos,
                                     self._ingreso_terminado))

    def _ingreso_terminado(self, mensaje):
        """Vuelve a la lista de habitaciones (con mensaje si se registro)."""
        self.abrir_habitaciones(mensaje)

    def abrir_salida(self):
        self.dialogos.ocultar()
        self._mostrar(VentanaSalida(self.hotel, self.dialogos))

    def action_performed(self, evento):
        if evento is self.item_menu1:
            self.abrir_habitaciones()
        if evento is self.item_menu2:
            self.abrir_salida()


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
def _debe_fallar(funcion, *args):
    try:
        funcion(*args)
    except ValueError:
        return
    raise AssertionError("debió lanzar ValueError")


def probar_modelo():
    hotel = Hotel()
    assert len(hotel.habitaciones) == 10
    assert hotel.habitaciones[0].precio_dia == 120000
    assert hotel.habitaciones[4].precio_dia == 120000
    assert hotel.habitaciones[5].precio_dia == 160000
    assert hotel.habitaciones[9].precio_dia == 160000

    # fechas
    assert convertir_fecha("2026-11-26") == date(2026, 11, 26)
    for mala in ["26-11-2026", "2026/11/26", "2026-13-01", "2026-02-30", "", "abc"]:
        _debe_fallar(convertir_fecha, mala)

    # huesped
    _debe_fallar(Huesped, "", "Ruiz", "123")
    _debe_fallar(Huesped, "Ana", "", "123")
    _debe_fallar(Huesped, "Ana", "Ruiz", "")
    _debe_fallar(Huesped, "Ana", "Ruiz", "12a")

    # ingreso
    ana = Huesped("Ana", "Ruiz", "1020304050")
    hotel.ingresar_huesped(2, ana, date(2026, 11, 20))
    assert hotel.habitaciones[1].esta_ocupada() and hotel.contar_ocupadas() == 1
    _debe_fallar(hotel.ingresar_huesped, 2, ana, date(2026, 11, 21))   # ocupada
    _debe_fallar(hotel.ingresar_huesped, 11, ana, date(2026, 11, 21))  # no existe
    _debe_fallar(hotel.ingresar_huesped, 0, ana, date(2026, 11, 21))

    # estadia y salida
    assert hotel.calcular_estadia(2, date(2026, 11, 23)) == (3, 360000)
    _debe_fallar(hotel.calcular_estadia, 2, date(2026, 11, 20))   # mismo dia
    _debe_fallar(hotel.calcular_estadia, 2, date(2026, 11, 10))   # anterior
    _debe_fallar(hotel.calcular_estadia, 3, date(2026, 11, 23))   # no ocupada
    hotel.ingresar_huesped(7, Huesped("Luis", "Soto", "99"), date(2026, 12, 30))
    assert hotel.calcular_estadia(7, date(2027, 1, 2)) == (3, 480000)  # cruza el año
    assert hotel.registrar_salida(2, date(2026, 11, 22)) == (2, 240000)
    assert not hotel.habitaciones[1].esta_ocupada()
    _debe_fallar(hotel.registrar_salida, 2, date(2026, 11, 22))   # ya libre
    print("OK  Modelo: habitaciones, precios, fechas, ingreso, estadía y salida")


def probar_interfaz():
    v = VentanaPrincipal()

    # --- Consultar habitaciones ---
    v.item_menu1.click()
    hab = v.ventana_actual
    assert len(hab.botones) == 10
    assert hab.botones[0].button_style == "success" and "Libre" in hab.botones[0].description

    # ingreso con errores
    hab.botones[0].click()
    ing = v.ventana_actual
    assert isinstance(ing, VentanaIngreso) and ing.numero == 1
    ing.fecha.value = "2026-11-20"
    ing.registrar.click()
    assert "obligatorios" in v.dialogos.mensaje.value
    ing.nombre.value, ing.apellidos.value, ing.documento.value = "Ana", "Ruiz", "12x"
    ing.registrar.click()
    assert "solo números" in v.dialogos.mensaje.value
    ing.documento.value = "1020304050"
    ing.fecha.value = "20/11/2026"
    ing.registrar.click()
    assert "aaaa-mm-dd" in v.dialogos.mensaje.value
    assert not v.hotel.habitaciones[0].esta_ocupada()
    ing.fecha.value = "2026-11-20"
    ing.registrar.click()
    assert v.hotel.habitaciones[0].esta_ocupada()
    assert isinstance(v.ventana_actual, VentanaHabitaciones)
    assert "Ingreso registrado" in v.dialogos.mensaje.value
    hab = v.ventana_actual
    assert hab.botones[0].button_style == "danger"
    assert "Ocupadas:</b> 1" in hab.resumen.value

    # habitacion ocupada -> error
    hab.botones[0].click()
    assert "está ocupada" in v.dialogos.mensaje.value
    assert isinstance(v.ventana_actual, VentanaHabitaciones)

    # cancelar ingreso
    hab.botones[6].click()
    v.ventana_actual.cancelar.click()
    assert isinstance(v.ventana_actual, VentanaHabitaciones)
    assert not v.hotel.habitaciones[6].esta_ocupada()

    # segunda habitacion (precio 160.000)
    hab.botones[6].click()
    ing = v.ventana_actual
    ing.fecha.value = "2026-11-21"
    ing.nombre.value, ing.apellidos.value, ing.documento.value = "Luis", "Soto", "777"
    ing.registrar.click()
    assert v.hotel.habitaciones[6].esta_ocupada()

    # --- Salida de huespedes ---
    v.item_menu2.click()
    sal = v.ventana_actual
    assert sal.fecha.disabled and sal.calcular.disabled and sal.registrar.disabled
    for malo, texto in [("", "válido"), ("abc", "válido"), ("0", "entre 1 y 10"),
                        ("11", "entre 1 y 10"), ("3", "no está ocupada")]:
        sal.numero.value = malo
        sal.buscar.click()
        assert texto in v.dialogos.mensaje.value, (malo, v.dialogos.mensaje.value)
        assert sal.fecha.disabled

    sal.numero.value = "1"
    sal.buscar.click()
    assert not sal.fecha.disabled and "Ana Ruiz" in sal.datos.value
    assert sal.calcular.disabled                      # fecha vacia
    sal.fecha.value = "2026-1-5"
    assert sal.calcular.disabled                      # formato invalido
    sal.fecha.value = "2026-11-20"
    assert not sal.calcular.disabled                  # formato valido
    sal.calcular.click()
    assert "posterior" in v.dialogos.mensaje.value and sal.registrar.disabled
    sal.fecha.value = "2026-11-25"
    sal.calcular.click()
    assert "Días de estadía:</b> 5" in sal.resultado.value
    assert "$600,000" in sal.resultado.value and not sal.registrar.disabled
    sal.fecha.value = "2026-11-26"                    # cambiar la fecha reinicia
    assert sal.registrar.disabled and sal.resultado.value == ""
    sal.calcular.click()
    assert "Días de estadía:</b> 6" in sal.resultado.value
    assert "$720,000" in sal.resultado.value and not sal.registrar.disabled
    sal.registrar.click()
    assert not v.hotel.habitaciones[0].esta_ocupada()
    assert "Salida registrada" in v.dialogos.mensaje.value
    assert sal.registrar.disabled and sal.fecha.disabled

    # habitacion 7: 4 dias a 160.000
    sal.numero.value = "7"
    sal.buscar.click()
    sal.fecha.value = "2026-11-25"
    sal.calcular.click()
    assert "Días de estadía:</b> 4" in sal.resultado.value and "$640,000" in sal.resultado.value
    sal.registrar.click()
    assert v.hotel.contar_ocupadas() == 0

    # tras salir, la habitacion queda libre en la vista de habitaciones
    v.item_menu1.click()
    assert all(b.button_style == "success" for b in v.ventana_actual.botones)
    print("OK  Interfaz: ingreso, errores, ocupada, salida, cálculo y liberación")


probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")
