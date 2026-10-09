from enum import Enum

class TipoCombustible(Enum):
    GASOLINA = "GASOLINA"
    BIOETANOL = "BIOETANOL"
    DIESEL = "DIESEL"
    BIODIESEL = "BIODIESEL"
    GAS_NATURAL = "GAS_NATURAL"

class TipoAutomovil(Enum):
    CIUDAD = "CIUDAD"
    SUBCOMPACTO = "SUBCOMPACTO"
    COMPACTO = "COMPACTO"
    FAMILIAR = "FAMILIAR"
    EJECUTIVO = "EJECUTIVO"
    SUV = "SUV"

class Color(Enum):
    BLANCO = "BLANCO"
    NEGRO = "NEGRO"
    ROJO = "ROJO"
    NARANJA = "NARANJA"
    AMARILLO = "AMARILLO"
    VERDE = "VERDE"
    AZUL = "AZUL"
    VIOLETA = "VIOLETA"

class Automovil:
    """Modela un automóvil. Los atributos llevan _ y se acceden con get/set."""

    def __init__(self, marca: str, modelo: int, motor: float,
                 tipo_combustible: TipoCombustible, tipo_automovil: TipoAutomovil,
                 numero_puertas: int, cantidad_asientos: int,
                 velocidad_maxima: int, color: Color):
        """Constructor. La velocidad actual inicia en 0."""
        self._marca = marca                          
        self._modelo = modelo                        
        self._motor = motor                          
        self._tipo_combustible = tipo_combustible    
        self._tipo_automovil = tipo_automovil        
        self._numero_puertas = numero_puertas
        self._cantidad_asientos = cantidad_asientos
        self._velocidad_maxima = velocidad_maxima   
        self._color = color                         
        self._velocidad_actual = 0                  

    def get_marca(self) -> str:
        return self._marca

    def get_modelo(self) -> int:
        return self._modelo

    def get_motor(self) -> float:
        return self._motor

    def get_tipo_combustible(self) -> TipoCombustible:
        return self._tipo_combustible

    def get_tipo_automovil(self) -> TipoAutomovil:
        return self._tipo_automovil

    def get_numero_puertas(self) -> int:
        return self._numero_puertas

    def get_cantidad_asientos(self) -> int:
        return self._cantidad_asientos

    def get_velocidad_maxima(self) -> int:
        return self._velocidad_maxima

    def get_color(self) -> Color:
        return self._color

    def get_velocidad_actual(self) -> int:
        return self._velocidad_actual

    def set_marca(self, marca: str) -> None:
        self._marca = marca

    def set_modelo(self, modelo: int) -> None:
        self._modelo = modelo

    def set_motor(self, motor: float) -> None:
        self._motor = motor

    def set_tipo_combustible(self, tipo_combustible: TipoCombustible) -> None:
        self._tipo_combustible = tipo_combustible

    def set_tipo_automovil(self, tipo_automovil: TipoAutomovil) -> None:
        self._tipo_automovil = tipo_automovil

    def set_numero_puertas(self, numero_puertas: int) -> None:
        self._numero_puertas = numero_puertas

    def set_cantidad_asientos(self, cantidad_asientos: int) -> None:
        self._cantidad_asientos = cantidad_asientos

    def set_velocidad_maxima(self, velocidad_maxima: int) -> None:
        self._velocidad_maxima = velocidad_maxima

    def set_color(self, color: Color) -> None:
        self._color = color

    def set_velocidad_actual(self, velocidad_actual: int) -> None:
        self._velocidad_actual = velocidad_actual

    def acelerar(self, incremento_velocidad: int) -> None:
        """Incrementa la velocidad sin superar la velocidad máxima."""
        if self._velocidad_actual + incremento_velocidad <= self._velocidad_maxima:
            self._velocidad_actual += incremento_velocidad
        else:
            print("No se puede incrementar a una velocidad superior a la máxima del automóvil.")

    def desacelerar(self, decremento_velocidad: int) -> None:
        """Decrementa la velocidad sin llegar a un valor negativo."""
        if self._velocidad_actual - decremento_velocidad >= 0:
            self._velocidad_actual -= decremento_velocidad
        else:
            print("No se puede decrementar a una velocidad negativa.")

    def frenar(self) -> None:
        """Coloca la velocidad actual en cero."""
        self._velocidad_actual = 0

    def calcular_tiempo_llegada(self, distancia: float):
        """Devuelve el tiempo estimado (horas) = distancia / velocidad actual.
        Si el automóvil está detenido no se puede calcular y devuelve None."""
        if self._velocidad_actual == 0:
            print("El automóvil está detenido: no es posible calcular el tiempo de llegada.")
            return None
        return distancia / self._velocidad_actual

    def imprimir(self) -> None:
        """Imprime en pantalla los valores de los atributos del automóvil."""
        print(f"Marca = {self._marca}")
        print(f"Modelo = {self._modelo}")
        print(f"Motor (litros) = {self._motor}")
        print(f"Tipo de combustible = {self._tipo_combustible.name}")
        print(f"Tipo de automóvil = {self._tipo_automovil.name}")
        print(f"Número de puertas = {self._numero_puertas}")
        print(f"Cantidad de asientos = {self._cantidad_asientos}")
        print(f"Velocidad máxima (km/h) = {self._velocidad_maxima}")
        print(f"Color = {self._color.name}")
        print(f"Velocidad actual (km/h) = {self._velocidad_actual}")

def main() -> None:
    """Crea un automóvil y realiza varios cambios en su velocidad."""
    auto1 = Automovil("Ford", 2018, 3, TipoCombustible.DIESEL,
                      TipoAutomovil.EJECUTIVO, 5, 6, 250, Color.NEGRO)
    auto1.imprimir()
    print()

    auto1.set_velocidad_actual(100)
    print(f"Velocidad actual = {auto1.get_velocidad_actual()} km/h")

    auto1.acelerar(20)
    print(f"Velocidad actual = {auto1.get_velocidad_actual()} km/h")

    auto1.desacelerar(50)
    print(f"Velocidad actual = {auto1.get_velocidad_actual()} km/h")

    print(f"Tiempo estimado para 140 km = {auto1.calcular_tiempo_llegada(140)} horas")

    auto1.frenar()
    print(f"Velocidad actual = {auto1.get_velocidad_actual()} km/h")

    auto1.desacelerar(20)   # Debe mostrar el mensaje de velocidad negativa
    print(f"Velocidad actual = {auto1.get_velocidad_actual()} km/h")

if __name__ == "__main__":
    main()
