"""
Desarrollador responsable: Santiago Loaiza Pérez

Jerarquía de servicios para Software FJ.
"""

from abc import ABC, abstractmethod
from typing import Any

from sistema_base import (
    EntidadBase,
    GestorLogs,
    ErrorValidacion,
    ErrorSistema,
    ErrorServicioNoDisponible,
)


# Excepciones

class ErrorPrecioInvalido(ErrorValidacion):
    """El precio ingresado no es válido."""


class ErrorDuracionInvalida(ErrorValidacion):
    """La duración ingresada no es válida."""


class ErrorDescuentoInvalido(ErrorValidacion):
    """El descuento ingresado no es válido."""


class ErrorTipoServicioDesconocido(ErrorValidacion):
    """El tipo de servicio no existe."""


# Clase base

class Servicio(EntidadBase, ABC):

    DESCUENTO_MAXIMO = 1.0
    IMPUESTO_MAXIMO = 2.0

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        precio_base: float,
        estado: str = "activo"
    ):
        super().__init__(id_servicio, estado)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ErrorValidacion(
                "El nombre del servicio no puede estar vacío"
            )

        self._nombre = nombre.strip()

        try:
            precio = float(precio_base)
        except (TypeError, ValueError) as e:
            raise ErrorPrecioInvalido(
                f"Precio inválido: {precio_base}"
            ) from e

        if precio <= 0:
            raise ErrorPrecioInvalido(
                "El precio debe ser mayor a cero"
            )

        self._precio_base = precio

        GestorLogs().registrar_evento(
            "SERVICIO",
            f"Servicio creado: {self._nombre}"
        )

    # Métodos abstractos

    @abstractmethod
    def calcular_costo(
        self,
        cantidad: float,
        descuento: float = 0.0,
        impuesto: float = 0.0
    ) -> float:
        ...

    @abstractmethod
    def validar(self) -> bool:
        ...

    @abstractmethod
    def obtener_descripcion(self) -> str:
        ...

    @abstractmethod
    def serializar(self) -> dict[str, Any]:
        ...
    
    # Validaciones compartidas
    
    def _validar_cantidad(
        self,
        cantidad: float,
        nombre_parametro: str = "cantidad"
    ) -> float:

        try:
            valor = float(cantidad)
        except (TypeError, ValueError) as e:
            raise ErrorDuracionInvalida(
                f"{nombre_parametro} debe ser numérico"
            ) from e

        if valor <= 0:
            raise ErrorDuracionInvalida(
                f"{nombre_parametro} debe ser mayor a cero"
            )

        return valor

    def _validar_descuento(self, descuento: float) -> float:

        try:
            valor = float(descuento)
        except (TypeError, ValueError) as e:
            raise ErrorDescuentoInvalido(
                "El descuento debe ser numérico"
            ) from e

        if not (0.0 <= valor <= self.DESCUENTO_MAXIMO):
            raise ErrorDescuentoInvalido(
                "El descuento está fuera de rango"
            )

        return valor

    def _validar_impuesto(self, impuesto: float) -> float:

        try:
            valor = float(impuesto)
        except (TypeError, ValueError) as e:
            raise ErrorValidacion(
                "El impuesto debe ser numérico"
            ) from e

        if not (0.0 <= valor <= self.IMPUESTO_MAXIMO):
            raise ErrorValidacion(
                "El impuesto está fuera de rango"
            )

        return valor

    def _aplicar_descuento_e_impuesto(
        self,
        subtotal: float,
        descuento: float,
        impuesto: float
    ) -> float:

        try:
            subtotal_descuento = subtotal * (1 - descuento)
            total = subtotal_descuento * (1 + impuesto)

            return round(total, 2)

        except Exception as e:
            raise ErrorSistema(
                "Error al calcular el total"
            ) from e

    # Propiedades
    
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float) -> None:

        try:
            precio = float(valor)
        except (TypeError, ValueError) as e:
            raise ErrorPrecioInvalido(
                "El precio debe ser numérico"
            ) from e

        if precio <= 0:
            raise ErrorPrecioInvalido(
                "El precio debe ser mayor a cero"
            )

        self._precio_base = precio

    # Estado

    def activar(self) -> None:
        self.cambiar_estado("activo")

    def desactivar(self) -> None:

        if not self.esta_activa():
            raise ErrorServicioNoDisponible(
                f"El servicio '{self._nombre}' ya está inactivo"
            )

        self.cambiar_estado("inactivo")

    def verificar_disponibilidad(self) -> None:

        if not self.esta_activa():
            raise ErrorServicioNoDisponible(
                f"El servicio '{self._nombre}' no está disponible"
            )

# ReservaSala

class ReservaSala(Servicio):

    MAX_HORAS = 24.0

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        precio_base: float,
        capacidad_personas: int = 10,
        estado: str = "activo"
    ):

        super().__init__(
            id_servicio,
            nombre,
            precio_base,
            estado
        )

        if not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            raise ErrorValidacion(
                "La capacidad debe ser un entero positivo"
            )

        self._capacidad_personas = capacidad_personas

    def calcular_costo(
        self,
        cantidad: float,
        descuento: float = 0.0,
        impuesto: float = 0.0
    ) -> float:

        self.verificar_disponibilidad()

        horas = self._validar_cantidad(cantidad, "horas")

        if horas > self.MAX_HORAS:
            raise ErrorDuracionInvalida(
                f"No se permiten más de {self.MAX_HORAS} horas"
            )

        descuento_val = self._validar_descuento(descuento)
        impuesto_val = self._validar_impuesto(impuesto)

        subtotal = self._precio_base * horas

        return self._aplicar_descuento_e_impuesto(
            subtotal,
            descuento_val,
            impuesto_val
        )

    def validar(self) -> bool:

        if self._precio_base <= 0:
            raise ErrorPrecioInvalido(
                "El precio debe ser mayor a cero"
            )

        if self._capacidad_personas <= 0:
            raise ErrorValidacion(
                "La capacidad debe ser mayor a cero"
            )

        return True

    def obtener_descripcion(self) -> str:

        return (
            f"[ReservaSala] {self._nombre} | "
            f"Precio/hora: ${self._precio_base:,.2f} | "
            f"Capacidad: {self._capacidad_personas} personas"
        )

    def serializar(self) -> dict[str, Any]:

        return {
            "tipo": "reserva_sala",
            "id": self.obtener_id(),
            "nombre": self._nombre,
            "precio_base": self._precio_base,
            "capacidad_personas": self._capacidad_personas,
            "estado": self.obtener_estado(),
            "fecha_creacion": self.obtener_fecha_creacion().isoformat(),
        }

    @property
    def capacidad_personas(self) -> int:
        return self._capacidad_personas

# AlquilerEquipo

class AlquilerEquipo(Servicio):

    TIPOS_EQUIPO_VALIDOS = {
        "proyector",
        "laptop",
        "camara",
        "audio",
        "videoconferencia",
        "otro",
    }

    MAX_DIAS = 30

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        precio_base: float,
        tipo_equipo: str = "otro",
        porcentaje_seguro: float = 0.05,
        estado: str = "activo"
    ):

        super().__init__(
            id_servicio,
            nombre,
            precio_base,
            estado
        )

        tipo = tipo_equipo.strip().lower()

        if tipo not in self.TIPOS_EQUIPO_VALIDOS:
            raise ErrorValidacion(
                "Tipo de equipo inválido"
            )

        self._tipo_equipo = tipo

        try:
            seguro = float(porcentaje_seguro)
        except (TypeError, ValueError) as e:
            raise ErrorValidacion(
                "El porcentaje de seguro debe ser numérico"
            ) from e

        if not (0.0 <= seguro <= 1.0):
            raise ErrorValidacion(
                "El porcentaje de seguro está fuera de rango"
            )

        self._porcentaje_seguro = seguro

    def calcular_costo(
        self,
        cantidad: float,
        descuento: float = 0.0,
        impuesto: float = 0.0,
        incluir_seguro: bool = False
    ) -> float:

        self.verificar_disponibilidad()

        dias = self._validar_cantidad(cantidad, "dias")

        if dias > self.MAX_DIAS:
            raise ErrorDuracionInvalida(
                f"No se permiten más de {self.MAX_DIAS} días"
            )

        descuento_val = self._validar_descuento(descuento)
        impuesto_val = self._validar_impuesto(impuesto)

        subtotal = self._precio_base * dias

        if incluir_seguro:
            subtotal += subtotal * self._porcentaje_seguro

        return self._aplicar_descuento_e_impuesto(
            subtotal,
            descuento_val,
            impuesto_val
        )

    def validar(self) -> bool:

        if self._tipo_equipo not in self.TIPOS_EQUIPO_VALIDOS:
            raise ErrorValidacion(
                "Tipo de equipo inválido"
            )

        return True

    def obtener_descripcion(self) -> str:

        return (
            f"[AlquilerEquipo] {self._nombre} | "
            f"Tipo: {self._tipo_equipo} | "
            f"Precio/día: ${self._precio_base:,.2f}"
        )

    def serializar(self) -> dict[str, Any]:

        return {
            "tipo": "alquiler_equipo",
            "id": self.obtener_id(),
            "nombre": self._nombre,
            "precio_base": self._precio_base,
            "tipo_equipo": self._tipo_equipo,
            "porcentaje_seguro": self._porcentaje_seguro,
            "estado": self.obtener_estado(),
            "fecha_creacion": self.obtener_fecha_creacion().isoformat(),
        }

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @property
    def porcentaje_seguro(self) -> float:
        return self._porcentaje_seguro

# AsesoriaEspecializada

class AsesoriaEspecializada(Servicio):

    ESPECIALIDADES = {
        "legal": 1.5,
        "tecnologia": 1.2,
        "financiera": 1.4,
        "marketing": 1.1,
        "general": 1.0,
    }

    MAX_HORAS = 8.0

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        precio_base: float,
        especialidad: str = "general",
        nombre_asesor: str = "Sin asignar",
        estado: str = "activo"
    ):

        super().__init__(
            id_servicio,
            nombre,
            precio_base,
            estado
        )

        especialidad_normalizada = especialidad.strip().lower()

        if especialidad_normalizada not in self.ESPECIALIDADES:
            raise ErrorValidacion(
                "Especialidad inválida"
            )

        self._especialidad = especialidad_normalizada
        self._multiplicador = self.ESPECIALIDADES[
            especialidad_normalizada
        ]

        if not isinstance(nombre_asesor, str) or not nombre_asesor.strip():
            raise ErrorValidacion(
                "El nombre del asesor no puede estar vacío"
            )

        self._nombre_asesor = nombre_asesor.strip()

    def calcular_costo(
        self,
        cantidad: float,
        descuento: float = 0.0,
        impuesto: float = 0.0
    ) -> float:

        self.verificar_disponibilidad()

        horas = self._validar_cantidad(cantidad, "horas")

        if horas > self.MAX_HORAS:
            raise ErrorDuracionInvalida(
                f"No se permiten más de {self.MAX_HORAS} horas"
            )

        descuento_val = self._validar_descuento(descuento)
        impuesto_val = self._validar_impuesto(impuesto)

        subtotal = (
            self._precio_base
            * self._multiplicador
            * horas
        )

        return self._aplicar_descuento_e_impuesto(
            subtotal,
            descuento_val,
            impuesto_val
        )

    def validar(self) -> bool:

        if self._especialidad not in self.ESPECIALIDADES:
            raise ErrorValidacion(
                "Especialidad inválida"
            )

        return True

    def obtener_descripcion(self) -> str:

        tarifa = self._precio_base * self._multiplicador

        return (
            f"[AsesoriaEspecializada] {self._nombre} | "
            f"Especialidad: {self._especialidad} | "
            f"Asesor: {self._nombre_asesor} | "
            f"Tarifa/hora: ${tarifa:,.2f}"
        )

    def serializar(self) -> dict[str, Any]:

        return {
            "tipo": "asesoria_especializada",
            "id": self.obtener_id(),
            "nombre": self._nombre,
            "precio_base": self._precio_base,
            "especialidad": self._especialidad,
            "multiplicador": self._multiplicador,
            "nombre_asesor": self._nombre_asesor,
            "estado": self.obtener_estado(),
            "fecha_creacion": self.obtener_fecha_creacion().isoformat(),
        }

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @property
    def nombre_asesor(self) -> str:
        return self._nombre_asesor

    @property
    def multiplicador(self) -> float:
        return self._multiplicador

# Fábrica de servicios
 
_MAPA_TIPOS = {
    "reserva_sala": ReservaSala,
    "alquiler_equipo": AlquilerEquipo,
    "asesoria_especializada": AsesoriaEspecializada,
}


def crear_servicio(
    id_servicio: str,
    nombre: str,
    precio_base: float,
    tipo: str = "reserva_sala",
    **kwargs: Any
) -> Servicio:

    tipo_normalizado = tipo.strip().lower()

    if tipo_normalizado not in _MAPA_TIPOS:
        raise ErrorTipoServicioDesconocido(
            f"Tipo desconocido: {tipo}"
        )

    clase_servicio = _MAPA_TIPOS[tipo_normalizado]

    return clase_servicio(
        id_servicio=id_servicio,
        nombre=nombre,
        precio_base=precio_base,
        **kwargs
    )


__all__ = [
    "ErrorPrecioInvalido",
    "ErrorDuracionInvalida",
    "ErrorDescuentoInvalido",
    "ErrorTipoServicioDesconocido",
    "Servicio",
    "ReservaSala",
    "AlquilerEquipo",
    "AsesoriaEspecializada",
    "crear_servicio",
]
