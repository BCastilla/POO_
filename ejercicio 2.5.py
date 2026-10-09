from enum import Enum

class TipoCuenta(Enum):
    AHORROS = "AHORROS"
    CORRIENTE = "CORRIENTE"
    
class CuentaBancaria:
    
    def __init__(self, nombres_titular: str, apellidos_titular: str,
                 numero_cuenta: int, tipo_cuenta: TipoCuenta):
        """Constructor. El saldo no se recibe: inicialmente es cero."""
        self.nombres_titular = nombres_titular
        self.apellidos_titular = apellidos_titular
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.saldo = 0.0

    def imprimir(self) -> None:
        """Imprime en pantalla los datos de la cuenta."""
        print(f"Nombres del titular = {self.nombres_titular}")
        print(f"Apellidos del titular = {self.apellidos_titular}")
        print(f"Número de cuenta = {self.numero_cuenta}")
        print(f"Tipo de cuenta = {self.tipo_cuenta.name}")
        print(f"Saldo = ${self.saldo:,.2f}")

    def consultar_saldo(self) -> None:
        """Imprime en pantalla el saldo actual."""
        print(f"El saldo actual es = ${self.saldo:,.2f}")

    def consignar(self, valor: float) -> bool:
        """Suma 'valor' al saldo. Devuelve True si la operación fue válida
        (el valor debe ser mayor que cero)."""
        if valor > 0:
            self.saldo += valor
            print(f"Se ha consignado ${valor:,.2f} en la cuenta. "
                  f"El nuevo saldo es ${self.saldo:,.2f}")
            return True
        print("El valor a consignar debe ser mayor que cero.")
        return False

    def retirar(self, valor: float) -> bool:
        """Resta 'valor' del saldo. Devuelve True si la operación fue válida
        (valor mayor que cero y no superior al saldo actual)."""
        if valor <= 0:
            print("El valor a retirar debe ser mayor que cero.")
            return False
        if valor > self.saldo:
            print("Fondos insuficientes: el valor a retirar supera el saldo actual.")
            return False
        self.saldo -= valor
        print(f"Se ha retirado ${valor:,.2f} de la cuenta. "
              f"El nuevo saldo es ${self.saldo:,.2f}")
        return True


def main() -> None:
    """Crea una cuenta y realiza operaciones de consignar y retirar."""
    cuenta = CuentaBancaria("Pedro", "Pérez", 123456789, TipoCuenta.AHORROS)
    cuenta.imprimir()
    print()
    cuenta.consignar(200000)
    cuenta.consignar(300000)
    cuenta.retirar(400000)
    cuenta.consultar_saldo()
    print()
    cuenta.retirar(500000)   # Supera el saldo: debe ser rechazado
    cuenta.consignar(-100)   # Valor inválido: debe ser rechazado


if __name__ == "__main__":
    main()
