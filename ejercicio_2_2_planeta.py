# -*- coding: utf-8 -*-
"""
Ejercicio 2.2 - Atributos con tipos primitivos y enumerados: clase Planeta

Un planeta tiene nombre, cantidad de satélites, masa (kg), volumen (km³),
diámetro (km), distancia media al Sol (km), tipo (enumerado) y si es
observable a simple vista. Se calcula su densidad y si es un planeta exterior
(más allá del cinturón de asteroides, que llega hasta 3.4 UA).

Ejecución en Colab:  %run ejercicio_2_2_planeta.py
"""

from enum import Enum


class TipoPlaneta(Enum):
    """Tipo de planeta de acuerdo con su tamaño."""
    GASEOSO = "GASEOSO"
    TERRESTRE = "TERRESTRE"
    ENANO = "ENANO"


class Planeta:
    """Modela un planeta del sistema solar."""

    UA_KM = 149_597_870                    # 1 Unidad Astronómica en km
    LIMITE_CINTURON_KM = UA_KM * 3.4       # Fin del cinturón de asteroides (3.4 UA)

    def __init__(self, nombre: str = None, cantidad_satelites: int = 0,
                 masa: float = 0, volumen: float = 0, diametro: int = 0,
                 distancia_sol: int = 0, tipo: TipoPlaneta = None,
                 es_observable: bool = False):
        """Constructor. Los valores por defecto son los valores iniciales del enunciado."""
        self.nombre = nombre                          # Nombre (inicial: None)
        self.cantidad_satelites = cantidad_satelites  # Satélites (inicial: 0)
        self.masa = masa                              # Masa en kg (inicial: 0)
        self.volumen = volumen                        # Volumen en km³ (inicial: 0)
        self.diametro = diametro                      # Diámetro en km (inicial: 0)
        self.distancia_sol = distancia_sol            # Distancia media al Sol en km (inicial: 0)
        self.tipo = tipo                              # Tipo de planeta (enumerado)
        self.es_observable = es_observable            # Observable a simple vista (inicial: False)

    def imprimir(self) -> None:
        """Imprime en pantalla los valores de los atributos del planeta."""
        print(f"Nombre del planeta = {self.nombre}")
        print(f"Cantidad de satélites = {self.cantidad_satelites}")
        print(f"Masa del planeta (kg) = {self.masa}")
        print(f"Volumen del planeta (km³) = {self.volumen}")
        print(f"Diámetro del planeta (km) = {self.diametro}")
        print(f"Distancia al sol (km) = {self.distancia_sol}")
        print(f"Tipo de planeta = {self.tipo.name if self.tipo else None}")
        print(f"Es observable = {self.es_observable}")

    def calcular_densidad(self) -> float:
        """Devuelve la densidad: cociente entre la masa y el volumen."""
        if self.volumen == 0:
            raise ValueError("El volumen debe ser mayor que cero para calcular la densidad.")
        return self.masa / self.volumen

    def es_planeta_exterior(self) -> bool:
        """Devuelve True si el planeta está más allá del cinturón de asteroides."""
        return self.distancia_sol > Planeta.LIMITE_CINTURON_KM


def main() -> None:
    """Crea dos planetas, imprime sus datos, su densidad y si son exteriores."""
    p1 = Planeta("Tierra", 1, 5.9736E24, 1.08321E12, 12742, 150_000_000,
                 TipoPlaneta.TERRESTRE, True)
    p1.imprimir()
    print(f"Densidad del planeta (kg/km³) = {p1.calcular_densidad():.4e}")
    print(f"Es planeta exterior = {p1.es_planeta_exterior()}")
    print()

    p2 = Planeta("Júpiter", 79, 1.899E27, 1.4313E15, 139820, 750_000_000,
                 TipoPlaneta.GASEOSO, True)
    p2.imprimir()
    print(f"Densidad del planeta (kg/km³) = {p2.calcular_densidad():.4e}")
    print(f"Es planeta exterior = {p2.es_planeta_exterior()}")


if __name__ == "__main__":
    main()
