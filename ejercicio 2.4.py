import math

class Circulo:
    """Círculo definido por su radio (cm)."""

    def __init__(self, radio: float):
        self.radio = radio

    def calcular_area(self) -> float:
        """Área = pi * radio²"""
        return math.pi * math.pow(self.radio, 2)

    def calcular_perimetro(self) -> float:
        """Perímetro = 2 * pi * radio"""
        return 2 * math.pi * self.radio

class Rectangulo:
    """Rectángulo definido por su base y altura (cm)."""

    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    def calcular_area(self) -> float:
        """Área = base * altura"""
        return self.base * self.altura

    def calcular_perimetro(self) -> float:
        """Perímetro = 2 * base + 2 * altura"""
        return 2 * self.base + 2 * self.altura


class Cuadrado:
    """Cuadrado definido por la longitud de su lado (cm)."""

    def __init__(self, lado: float):
        self.lado = lado

    def calcular_area(self) -> float:
        """Área = lado²"""
        return self.lado * self.lado

    def calcular_perimetro(self) -> float:
        """Perímetro = 4 * lado"""
        return 4 * self.lado


class TrianguloRectangulo:
    """Triángulo rectángulo definido por su base y altura (catetos, en cm)."""

    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    def calcular_hipotenusa(self) -> float:
        """Teorema de Pitágoras: hipotenusa = raíz(base² + altura²)"""
        return math.sqrt(self.base ** 2 + self.altura ** 2)

    def calcular_area(self) -> float:
        """Área = (base * altura) / 2"""
        return self.base * self.altura / 2

    def calcular_perimetro(self) -> float:
        """Perímetro = base + altura + hipotenusa"""
        return self.base + self.altura + self.calcular_hipotenusa()

    def determinar_tipo_triangulo(self) -> str:
        """Clasifica el triángulo según sus tres lados (base, altura, hipotenusa).
        Nota: en un triángulo rectángulo la hipotenusa siempre es mayor que cada
        cateto, así que en la práctica solo resultan escaleno o isósceles."""
        a, b, c = self.base, self.altura, self.calcular_hipotenusa()
        ab = math.isclose(a, b)
        ac = math.isclose(a, c)
        bc = math.isclose(b, c)
        if ab and ac and bc:
            return "equilátero"      # Los tres lados iguales
        if not ab and not ac and not bc:
            return "escaleno"        # Los tres lados diferentes
        return "isósceles"           # Exactamente dos lados iguales


class PruebaFiguras:
    """Clase de prueba: contiene el método main (punto de entrada)."""

    @staticmethod
    def main() -> None:
        figura1 = Circulo(2)
        figura2 = Rectangulo(1, 2)
        figura3 = Cuadrado(3)
        figura4 = TrianguloRectangulo(3, 5)

        print(f"El área del círculo es = {figura1.calcular_area()}")
        print(f"El perímetro del círculo es = {figura1.calcular_perimetro()}")
        print()
        print(f"El área del rectángulo es = {figura2.calcular_area()}")
        print(f"El perímetro del rectángulo es = {figura2.calcular_perimetro()}")
        print()
        print(f"El área del cuadrado es = {figura3.calcular_area()}")
        print(f"El perímetro del cuadrado es = {figura3.calcular_perimetro()}")
        print()
        print(f"El área del triángulo es = {figura4.calcular_area()}")
        print(f"El perímetro del triángulo es = {figura4.calcular_perimetro()}")
        print(f"La hipotenusa del triángulo es = {figura4.calcular_hipotenusa()}")
        print(f"Es un triángulo {figura4.determinar_tipo_triangulo()}")

        # Prueba extra: catetos iguales -> triángulo isósceles
        figura5 = TrianguloRectangulo(4, 4)
        print(f"El triángulo (4, 4) es {figura5.determinar_tipo_triangulo()}")


if __name__ == "__main__":
    PruebaFiguras.main()
