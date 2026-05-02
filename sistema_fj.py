# Sistema Software FJ
# Tarea 4 - Manejo de excepciones y Programación Orientada a Objetos

from abc import ABC, abstractmethod


# Excepción personalizada para errores del sistema
class ErrorSistema(Exception):
    pass


# Clase Cliente
class Cliente:
    def __init__(self, nombre, cedula):
        if nombre == "":
            raise ErrorSistema("El nombre del cliente no puede estar vacío.")

        if not cedula.isdigit():
            raise ErrorSistema("La cédula debe contener solo números.")

        self.__nombre = nombre
        self.__cedula = cedula

    def obtener_nombre(self):
        return self.__nombre

    def obtener_cedula(self):
        return self.__cedula

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} - Cédula: {self.__cedula}"


# Clase abstracta Servicio
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        if precio_base <= 0:
            raise ErrorSistema("El precio del servicio debe ser mayor que cero.")

        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# Servicio 1: Reserva de sala
class ReservaSala(Servicio):
    def calcular_costo(self, horas):
        if horas <= 0:
            raise ErrorSistema("Las horas de reserva deben ser mayores que cero.")
        return self.precio_base * horas

    def descripcion(self):
        return "Servicio de reserva de sala"


# Servicio 2: Alquiler de equipo
class AlquilerEquipo(Servicio):
    def calcular_costo(self, horas):
        if horas <= 0:
            raise ErrorSistema("Las horas de alquiler deben ser mayores que cero.")
        return self.precio_base * horas

    def descripcion(self):
        return "Servicio de alquiler de equipo"


# Servicio 3: Asesoría especializada
class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, horas):
        if horas <= 0:
            raise ErrorSistema("Las horas de asesoría deben ser mayores que cero.")
        return self.precio_base * horas

    def descripcion(self):
        return "Servicio de asesoría especializada"


# Clase Reserva
class Reserva:
    def __init__(self, cliente, servicio, horas):
        if not isinstance(cliente, Cliente):
            raise ErrorSistema("El cliente no es válido.")

        if not isinstance(servicio, Servicio):
            raise ErrorSistema("El servicio no es válido.")

        if horas <= 0:
            raise ErrorSistema("La duración de la reserva debe ser mayor que cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def procesar_reserva(self):
        costo = self.servicio.calcular_costo(self.horas)
        self.confirmar()
        return costo

    def mostrar_reserva(self):
        return (
            f"{self.cliente.mostrar_info()} | "
            f"Servicio: {self.servicio.descripcion()} | "
            f"Horas: {self.horas} | "
            f"Estado: {self.estado}"
        )
    
def guardar_log(mensaje):
    with open("registro_eventos.log", "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")

# Programa principal de prueba
print("Bienvenido al sistema Software FJ")
print("Pruebas del sistema con manejo de excepciones\n")

operaciones = [
    ("1. Cliente válido y reserva de sala", lambda: Reserva(Cliente("José Herrera", "1075237583"), ReservaSala("Sala de reuniones", 30000), 2)),
    ("2. Cliente con nombre vacío", lambda: Cliente("", "1075237583")),
    ("3. Cliente con cédula inválida", lambda: Cliente("Carlos Pérez", "ABC123")),
    ("4. Servicio con precio inválido", lambda: ReservaSala("Sala pequeña", -10000)),
    ("5. Reserva con horas negativas", lambda: Reserva(Cliente("Ana Gómez", "123456789"), ReservaSala("Sala VIP", 40000), -2)),
    ("6. Alquiler de equipo correcto", lambda: Reserva(Cliente("Laura Díaz", "987654321"), AlquilerEquipo("Portátil", 25000), 3)),
    ("7. Asesoría especializada correcta", lambda: Reserva(Cliente("Miguel Torres", "456789123"), AsesoriaEspecializada("Asesoría Python", 50000), 2)),
    ("8. Reserva con cliente inválido", lambda: Reserva("Cliente incorrecto", ReservaSala("Sala A", 20000), 1)),
    ("9. Reserva con servicio inválido", lambda: Reserva(Cliente("Sofía Rojas", "789123456"), "Servicio incorrecto", 1)),
    ("10. Reserva cancelada correctamente", lambda: Reserva(Cliente("Pedro Ruiz", "321654987"), ReservaSala("Sala ejecutiva", 35000), 1)),
]

for nombre_operacion, operacion in operaciones:
    print(nombre_operacion)

    try:
        resultado = operacion()

    except ErrorSistema as error:
        print("Error controlado:", error)
        guardar_log(f"{nombre_operacion} - Error controlado: {error}")

    except Exception as error:
        print("Error inesperado:", error)
        guardar_log(f"{nombre_operacion} - Error inesperado: {error}")

    else:
        if isinstance(resultado, Reserva):
            costo = resultado.procesar_reserva()

            if "cancelada" in nombre_operacion.lower():
                resultado.cancelar()

            print("Operación realizada correctamente.")
            print(resultado.mostrar_reserva())
            print("Costo total:", costo)
            guardar_log(f"{nombre_operacion} - Operación exitosa")
        else:
            print("Operación realizada correctamente.")
            guardar_log(f"{nombre_operacion} - Operación exitosa")

    finally:
        print("Prueba finalizada.\n")

print("Fin de las 10 pruebas del sistema.")