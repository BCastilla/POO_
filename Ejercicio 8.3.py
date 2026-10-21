import io
import math
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from IPython.display import display


# Jerarquia de clases 
def validar_positivo(nombre, valor):
    """Lanza ValueError si la medida no es un numero mayor que cero."""
    if not (valor > 0 and math.isfinite(valor)):
        raise ValueError(f"{nombre} debe ser un número mayor que cero.")


class FiguraGeometrica:
    """Figura geometrica con un volumen y una superficie que seran
    calculados segun el tipo de figura (clase padre)."""

    def __init__(self):
        self._volumen = 0.0      # volumen de la figura
        self._superficie = 0.0   # superficie de la figura

    def set_volumen(self, volumen):
        self._volumen = volumen

    def set_superficie(self, superficie):
        self._superficie = superficie

    def get_volumen(self):
        return self._volumen

    def get_superficie(self):
        return self._superficie


class Cilindro(FiguraGeometrica):
    """Subclase de FiguraGeometrica con un radio y una altura."""

    def __init__(self, radio, altura):
        super().__init__()
        validar_positivo("El radio", radio)
        validar_positivo("La altura", altura)
        self.radio = radio
        self.altura = altura
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return math.pi * self.altura * math.pow(self.radio, 2.0)

    def calcular_superficie(self):
        area_lado_a = 2.0 * math.pi * self.radio * self.altura
        area_lado_b = 2.0 * math.pi * math.pow(self.radio, 2.0)
        return area_lado_a + area_lado_b


class Esfera(FiguraGeometrica):
    """Subclase de FiguraGeometrica con un radio."""

    def __init__(self, radio):
        super().__init__()
        validar_positivo("El radio", radio)
        self.radio = radio
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return (4.0 / 3.0) * math.pi * math.pow(self.radio, 3.0)

    def calcular_superficie(self):
        return 4.0 * math.pi * math.pow(self.radio, 2.0)


class Piramide(FiguraGeometrica):

    def __init__(self, base, altura, apotema):
        super().__init__()
        validar_positivo("La base", base)
        validar_positivo("La altura", altura)
        validar_positivo("El apotema", apotema)
        self.base = base
        self.altura = altura
        self.apotema = apotema
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return (math.pow(self.base, 2.0) * self.altura) / 3.0

    def calcular_superficie(self):
        area_base = math.pow(self.base, 2.0)
        area_lado = 2.0 * self.base * self.apotema
        return area_base + area_lado


# ---- Parte propuesta: otras figuras geometricas ----
class Cubo(FiguraGeometrica):

    def __init__(self, arista):
        super().__init__()
        validar_positivo("La arista", arista)
        self.arista = arista
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return math.pow(self.arista, 3.0)

    def calcular_superficie(self):
        return 6.0 * math.pow(self.arista, 2.0)


class Prisma(FiguraGeometrica):

    def __init__(self, largo, ancho, alto):
        super().__init__()
        validar_positivo("El largo", largo)
        validar_positivo("El ancho", ancho)
        validar_positivo("El alto", alto)
        self.largo = largo
        self.ancho = ancho
        self.alto = alto
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        return self.largo * self.ancho * self.alto

    def calcular_superficie(self):
        return 2.0 * (self.largo * self.ancho + self.largo * self.alto
                      + self.ancho * self.alto)


# ---- Parte propuesta: Imagenes de cada figura ---- 

def _caja(ax, l, a, h, color):
    """Dibuja un paralelepipedo (sirve para el cubo y el prisma)."""
    v = np.array([[0, 0, 0], [l, 0, 0], [l, a, 0], [0, a, 0],
                  [0, 0, h], [l, 0, h], [l, a, h], [0, a, h]])
    caras = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
             [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4]]
    ax.add_collection3d(Poly3DCollection([v[c] for c in caras], facecolors=color,
                                         edgecolors="k", alpha=0.8))
    m = max(l, a, h)
    ax.set_xlim(0, m); ax.set_ylim(0, m); ax.set_zlim(0, m)


def imagen_figura(tipo):
    """Genera la imagen (PNG en bytes) de la figura indicada."""
    fig = plt.figure(figsize=(3, 3), dpi=100)
    ax = fig.add_subplot(111, projection="3d")
    t = np.linspace(0, 2 * np.pi, 40)

    if tipo == "cilindro":
        z = np.linspace(0, 2, 2)
        T, Z = np.meshgrid(t, z)
        ax.plot_surface(np.cos(T), np.sin(T), Z, color="tab:blue", alpha=0.8)
        for zz in (0, 2):   # tapas inferior y superior
            tapa = [list(zip(np.cos(t), np.sin(t), zz * np.ones_like(t)))]
            ax.add_collection3d(Poly3DCollection(tapa, facecolors="tab:blue",
                                                 edgecolors="k", alpha=0.9))
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(-0.2, 2.2)
    elif tipo == "esfera":
        u, w = np.meshgrid(np.linspace(0, 2 * np.pi, 40), np.linspace(0, np.pi, 20))
        ax.plot_surface(np.cos(u) * np.sin(w), np.sin(u) * np.sin(w), np.cos(w),
                        color="tab:orange", alpha=0.85)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
    elif tipo == "piramide":
        p = np.array([[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0], [1, 1, 2.5]])
        caras = [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]
        ax.add_collection3d(Poly3DCollection([p[c] for c in caras],
                                             facecolors="tab:green", edgecolors="k",
                                             alpha=0.8))
        ax.set_xlim(0, 3); ax.set_ylim(0, 3); ax.set_zlim(0, 3)
    elif tipo == "cubo":
        _caja(ax, 2, 2, 2, "tab:red")
    elif tipo == "prisma":
        _caja(ax, 3, 2, 1.2, "tab:purple")

    ax.set_box_aspect((1, 1, 1))   # ejes con la misma proporcion
    ax.set_axis_off()
    ax.view_init(elev=20, azim=35)
    fig.tight_layout(pad=0)
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", transparent=True)
    plt.close(fig)
    return buffer.getvalue()


#Ventanas de cada figura 
class VentanaFigura:
    TITULO = ""
    TIPO_IMAGEN = ""
    CAMPOS = []   # lista de (etiqueta, nombre)

    def __init__(self):
        estilo = {"description_width": "100px"}
        caja = widgets.Layout(width="260px")
        self.campos = [widgets.Text(description=etiqueta, style=estilo, layout=caja)
                       for etiqueta, _ in self.CAMPOS]
        self.calcular = widgets.Button(description="Calcular", button_style="success")
        self.alerta = widgets.HTML("")
        self.volumen = widgets.Label("Volumen (cm3): ")
        self.superficie = widgets.Label("Superficie (cm2): ")
        self.imagen = widgets.Image(value=imagen_figura(self.TIPO_IMAGEN),
                                    format="png", width=170, height=170)
        self.calcular.on_click(self.action_performed)
        izquierda = widgets.VBox(
            [widgets.HTML(f"<h3 style='margin:0'>{self.TITULO}</h3>")]
            + self.campos + [self.calcular, self.alerta, self.volumen, self.superficie])
        self.contenedor = widgets.HBox([izquierda, self.imagen],
                                       layout=widgets.Layout(border="1px solid #888",
                                                             padding="12px"))

    def crear_figura(self, valores):
        """Cada ventana concreta crea su figura con los valores ingresados."""
        raise NotImplementedError

    def _leer_valores(self):
        valores = []
        for campo in self.campos:
            try:
                valor = float(campo.value.strip().replace(",", "."))
            except ValueError:
                raise ValueError("Campo nulo o error en formato de número.") from None
            if not math.isfinite(valor):
                raise ValueError("Campo nulo o error en formato de número.")
            valores.append(valor)
        return valores

    def action_performed(self, evento):
        self.alerta.value = ""
        try:
            figura = self.crear_figura(self._leer_valores())
        except ValueError as error:
            self.volumen.value = "Volumen (cm3): "
            self.superficie.value = "Superficie (cm2): "
            self.alerta.value = ("<div style='background:#fdecea;color:#b71c1c;"
                                 "border:1px solid #f44336;border-radius:4px;"
                                 f"padding:6px;margin:6px 0;max-width:250px'>"
                                 f"&#9888; {error}</div>")
            return
        self.volumen.value = f"Volumen (cm3): {figura.get_volumen():.2f}"
        self.superficie.value = f"Superficie (cm2): {figura.get_superficie():.2f}"


class VentanaCilindro(VentanaFigura):
    TITULO = "Cilindro"
    TIPO_IMAGEN = "cilindro"
    CAMPOS = [("Radio (cms):", "radio"), ("Altura (cms):", "altura")]
    def crear_figura(self, v): return Cilindro(v[0], v[1])


class VentanaEsfera(VentanaFigura):
    TITULO = "Esfera"
    TIPO_IMAGEN = "esfera"
    CAMPOS = [("Radio (cms):", "radio")]
    def crear_figura(self, v): return Esfera(v[0])


class VentanaPiramide(VentanaFigura):
    TITULO = "Pirámide"
    TIPO_IMAGEN = "piramide"
    CAMPOS = [("Base (cms):", "base"), ("Altura (cms):", "altura"),
              ("Apotema (cms):", "apotema")]
    def crear_figura(self, v): return Piramide(v[0], v[1], v[2])


class VentanaCubo(VentanaFigura):
    TITULO = "Cubo"
    TIPO_IMAGEN = "cubo"
    CAMPOS = [("Arista (cms):", "arista")]
    def crear_figura(self, v): return Cubo(v[0])


class VentanaPrisma(VentanaFigura):
    TITULO = "Prisma rectangular"
    TIPO_IMAGEN = "prisma"
    CAMPOS = [("Largo (cms):", "largo"), ("Ancho (cms):", "ancho"),
              ("Alto (cms):", "alto")]
    def crear_figura(self, v): return Prisma(v[0], v[1], v[2])

# VentanaPrincipal (menu) y Principal (main)
class VentanaPrincipal:

    def __init__(self):
        self.cilindro = widgets.Button(description="Cilindro")
        self.esfera = widgets.Button(description="Esfera")
        self.piramide = widgets.Button(description="Pirámide")
        self.cubo = widgets.Button(description="Cubo")
        self.prisma = widgets.Button(description="Prisma")
        self._botones = [self.cilindro, self.esfera, self.piramide,
                         self.cubo, self.prisma]
        for boton in self._botones:
            boton.on_click(self.action_performed)
        self.zona_ventana = widgets.VBox([])   # aqui aparece la ventana elegida
        self.ventana_actual = None
        self.contenedor = widgets.VBox(
            [widgets.HTML("<h3 style='margin:0'>Figuras</h3>"),
             widgets.HBox(self._botones), self.zona_ventana],
            layout=widgets.Layout(border="1px solid #888", padding="12px"))

    def action_performed(self, evento):
        if evento is self.esfera:
            self.ventana_actual = VentanaEsfera()
        if evento is self.cilindro:
            self.ventana_actual = VentanaCilindro()
        if evento is self.piramide:
            self.ventana_actual = VentanaPiramide()
        if evento is self.cubo:
            self.ventana_actual = VentanaCubo()
        if evento is self.prisma:
            self.ventana_actual = VentanaPrisma()
        self.zona_ventana.children = [self.ventana_actual.contenedor]


class Principal:

    @staticmethod
    def main():
        mi_ventana_principal = VentanaPrincipal()
        display(mi_ventana_principal.contenedor)
        return mi_ventana_principal

mi_ventana = Principal.main()

# Verificacion automatica
def casi(a, b):
    return abs(a - b) < 1e-6

def probar_modelo():
    c = Cilindro(2, 5)
    assert casi(c.get_volumen(), 62.831853) and casi(c.get_superficie(), 87.964594)
    e = Esfera(3)
    assert casi(e.get_volumen(), 113.097336) and casi(e.get_superficie(), 113.097336)
    p = Piramide(4, 6, 7)
    assert casi(p.get_volumen(), 32.0) and casi(p.get_superficie(), 72.0)
    k = Cubo(3)
    assert casi(k.get_volumen(), 27.0) and casi(k.get_superficie(), 54.0)
    r = Prisma(2, 3, 4)
    assert casi(r.get_volumen(), 24.0) and casi(r.get_superficie(), 52.0)
    print("OK  Cálculos de cilindro, esfera, pirámide, cubo y prisma")

    # Herencia y polimorfismo
    figuras = [c, e, p, k, r]
    assert all(isinstance(f, FiguraGeometrica) for f in figuras)
    assert all(f.get_volumen() > 0 and f.get_superficie() > 0 for f in figuras)
    print("OK  Herencia: todas son FiguraGeometrica")

    # Validaciones
    for construir in (lambda: Cilindro(-1, 2), lambda: Esfera(0), lambda: Cubo(-3)):
        try:
            construir()
            raise AssertionError("debió lanzar ValueError")
        except ValueError:
            pass
    print("OK  Validación de medidas no positivas")

def probar_interfaz():
    # Cada ventana: datos validos
    casos = [(VentanaCilindro, ["2", "5"], "62.83", "87.96"),
             (VentanaEsfera, ["3"], "113.10", "113.10"),
             (VentanaPiramide, ["4", "6", "7"], "32.00", "72.00"),
             (VentanaCubo, ["3"], "27.00", "54.00"),
             (VentanaPrisma, ["2", "3", "4"], "24.00", "52.00")]
    for clase, datos, vol, sup in casos:
        v = clase()
        for campo, dato in zip(v.campos, datos):
            campo.value = dato
        v.calcular.click()
        assert v.volumen.value == f"Volumen (cm3): {vol}", (clase.__name__, v.volumen.value)
        assert v.superficie.value == f"Superficie (cm2): {sup}"
        assert v.alerta.value == ""
        assert len(v.imagen.value) > 1000      # la imagen se genero
    print("OK  Las 5 ventanas calculan y muestran su imagen")

    # Errores: texto, vacio y negativo
    v = VentanaCilindro()
    v.campos[0].value, v.campos[1].value = "abc", "5"
    v.calcular.click()
    assert "formato de número" in v.alerta.value
    v.campos[0].value, v.campos[1].value = "", "5"
    v.calcular.click()
    assert "formato de número" in v.alerta.value
    v.campos[0].value, v.campos[1].value = "-2", "5"
    v.calcular.click()
    assert "mayor que cero" in v.alerta.value
    print("OK  Alertas por dato no numérico, vacío y negativo")

    # Menu principal
    m = VentanaPrincipal()
    for boton, clase in [(m.cilindro, VentanaCilindro), (m.esfera, VentanaEsfera),
                         (m.piramide, VentanaPiramide), (m.cubo, VentanaCubo),
                         (m.prisma, VentanaPrisma)]:
        boton.click()
        assert isinstance(m.ventana_actual, clase)
        assert m.zona_ventana.children[0] is m.ventana_actual.contenedor
    print("OK  El menú principal abre cada ventana")

probar_modelo()
probar_interfaz()
print("\nTODAS LAS PRUEBAS PASARON")

# DEMO
"""Demo para probar que cada ventana funciona correctamente."""
datos_demo = [(VentanaCilindro, ["2", "5"]), (VentanaEsfera, ["3"]),
              (VentanaPiramide, ["4", "6", "7"]), (VentanaCubo, ["3"]),
              (VentanaPrisma, ["2", "3", "4"])]
for clase, datos in datos_demo:
    ventana = clase()
    for campo, dato in zip(ventana.campos, datos):
        campo.value = dato
    ventana.calcular.click()
    display(ventana.contenedor)
