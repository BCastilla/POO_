"""
Esta clase define objetos de tipo Persona con un nombre, apellidos,
número de documento de identidad y año de nacimiento.
Ejercicio 2.1. Definición de clases.
"""


class Persona:
    def __init__(self, nombre: str, apellidos: str,
                 num_documento_identidad: str, anyo_nacimiento: int):
        """Constructor que inicializa los atributos de la persona."""
        self.nombre = nombre                                  # Nombre
        self.apellidos = apellidos                            # Apellidos
        self.num_documento_identidad = num_documento_identidad  # Documento
        self.anyo_nacimiento = anyo_nacimiento                # Año de nacimiento

    def imprimir(self) -> None:
        """Imprime en pantalla los valores de los atributos del objeto."""
        print(f"Nombre = {self.nombre}")
        print(f"Apellidos = {self.apellidos}")
        print(f"Número de documento de identidad = {self.num_documento_identidad}")
        print(f"Año de nacimiento = {self.anyo_nacimiento}")


def main() -> None:
    """Crea dos personas y muestra los valores de sus atributos."""
    persona1 = Persona("Luis", "Pérez Gómez", "79345678", 1990)
    persona2 = Persona("Ana", "Torres Ruiz", "52987654", 1985)

    persona1.imprimir()
    print()
    persona2.imprimir()


if __name__ == "__main__":
    main()
