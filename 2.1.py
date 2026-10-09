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
    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")
    documento = input("Documento de identidad: ")
    anyo = int(input("Año de nacimiento: "))

    persona = Persona(nombre, apellidos, documento, anyo)
    print()
    persona.imprimir()

if __name__ == "__main__":
    main()
