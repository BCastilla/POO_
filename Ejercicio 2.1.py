class Persona:

    def __init__(self, nombre: str, apellidos: str,
                 numero_documento_identidad: str, ano_nacimiento: int):
        """Constructor: inicializa los atributos de la persona."""
        self.nombre = nombre                                          # Nombre
        self.apellidos = apellidos                                    # Apellidos
        self.numero_documento_identidad = numero_documento_identidad  # Documento
        self.ano_nacimiento = ano_nacimiento                          # Año de nacimiento

    def imprimir(self) -> None:
        """Imprime en pantalla los valores de los atributos de la persona."""
        print(f"Nombre = {self.nombre}")
        print(f"Apellidos = {self.apellidos}")
        print(f"Número de documento de identidad = {self.numero_documento_identidad}")
        print(f"Año de nacimiento = {self.ano_nacimiento}")
        print()


def main() -> None:
    """Crea dos personas e imprime sus datos en pantalla."""
    p1 = Persona("Pedro", "Pérez", "1053121010", 1998)
    p2 = Persona("Luis", "León", "1053223344", 2001)
    p1.imprimir()
    p2.imprimir()


if __name__ == "__main__":
    main()
