
from enum import Enum


class TipoPlaneta(Enum):
    GASEOSO = "GASEOSO"
    TERRESTRE = "TERRESTRE"
    ENANO = "ENANO"


class Planeta:
    # Una unidad astronómica (UA) = 149 597 870 km, en millones de km
    UA_EN_MILLONES_KM = 149.59787
    # El cinturón de asteroides se encuentra entre 2.1 y 3.4 UA
    LIMITE_CINTURON_UA = 3.4

    def __init__(self, nombre: str | None = None, satelites: int = 0,
                 masa: float = 0.0, volumen: float = 0.0, diametro: int = 0,
                 distancia_sol: int = 0, tipo: TipoPlaneta | None = None,
                 observable: bool = False):
        """Constructor que inicializa los atributos del planeta."""
        self.nombre = nombre                # Nombre del planeta
        self.satelites = satelites          # Cantidad de satélites
        self.masa = masa                    # Masa en kilogramos
        self.volumen = volumen              # Volumen en kilómetros cúbicos
        self.diametro = diametro            # Diámetro en kilómetros
        self.distancia_sol = distancia_sol  # Distancia media al Sol (millones km)
        self.tipo = tipo                    # Tipo de planeta según su tamaño
        self.observable = observable        # Observable a simple vista

    def imprimir(self) -> None:
        """Imprime en pantalla los valores de los atributos del planeta."""
        print(f"Nombre = {self.nombre}")
        print(f"Cantidad de satélites = {self.satelites}")
        print(f"Masa = {self.masa:.4e} kg")
        print(f"Volumen = {self.volumen:.4e} km³")
        print(f"Diámetro = {self.diametro} km")
        print(f"Distancia media al Sol = {self.distancia_sol} millones de km")
        print(f"Tipo de planeta = {self.tipo.name if self.tipo else None}")
        print(f"Observable a simple vista = {self.observable}")

    def calcular_densidad(self) -> float:
        """Densidad = masa / volumen (en kg/km³)."""
        if self.volumen == 0:
            return 0.0
        return self.masa / self.volumen

    def es_exterior(self) -> bool:
        """Un planeta es exterior si está más allá del cinturón de asteroides."""
        distancia_ua = self.distancia_sol / Planeta.UA_EN_MILLONES_KM
        return distancia_ua > Planeta.LIMITE_CINTURON_UA


def main() -> None:
    """Crea dos planetas y muestra sus atributos, densidad y si es exterior."""
    marte = Planeta("Marte", 2, 6.417e23, 1.6318e11, 6792, 228,
                    TipoPlaneta.TERRESTRE, True)
    # Júpiter: cantidad de satélites reportada en 2023
    jupiter = Planeta("Júpiter", 95, 1.898e27, 1.4313e15, 142984, 778,
                      TipoPlaneta.GASEOSO, True)

    for planeta in (marte, jupiter):
        planeta.imprimir()
        print(f"Densidad = {planeta.calcular_densidad():.4e} kg/km³")
        print(f"¿Es planeta exterior? {'Sí' if planeta.es_exterior() else 'No'}")
        print()


if __name__ == "__main__":
    main()
