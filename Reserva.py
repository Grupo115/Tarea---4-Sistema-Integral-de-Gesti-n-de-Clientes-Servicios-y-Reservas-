from datetime import datetime
from typing import Dict, Any

from sistema_base import (
    EntidadBase,
    ErrorReservaInvalida,
    ErrorOperacionNoPermitida,
)


class Reserva(EntidadBase):
    """
    Stub de Reserva para demostración del simulador.
    Será reemplazado por la clase real del compañero encargado de reservas.
    """

    ESTADOS_RESERVA = {'pendiente', 'confirmada', 'cancelada', 'completada'}

    def __init__(
        self,
        id_reserva: str,
        cliente,
        servicio,
        duracion: float,
        fecha_inicio: datetime,
    ):
        super().__init__(id_reserva, estado='activo')
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.fecha_inicio = fecha_inicio
        self.costo_total = 0.0
        self.estado_reserva = 'pendiente'
        self.validar()

    def validar(self) -> bool:
        if not hasattr(self.cliente, '_id'):
            raise ErrorReservaInvalida("Cliente debe ser un objeto con método _id")
        if not hasattr(self.servicio, '_id'):
            raise ErrorReservaInvalida("Servicio debe ser un objeto con método _id")
        if self.duracion <= 0:
            raise ErrorReservaInvalida(f"Duración debe ser positiva: {self.duracion}")
        if not isinstance(self.fecha_inicio, datetime):
            raise ErrorReservaInvalida("Fecha de inicio debe ser un datetime")
        return True

    def confirmar(self) -> None:
        if self.estado_reserva == 'confirmada':
            raise ErrorOperacionNoPermitida("La reserva ya está confirmada")
        if self.estado_reserva == 'cancelada':
            raise ErrorOperacionNoPermitida("No se puede confirmar una reserva cancelada")
        self.costo_total = self.servicio.calcular_costo(self.duracion, 0.0, 0.0)
        self.estado_reserva = 'confirmada'

    def cancelar(self) -> None:
        if self.estado_reserva == 'cancelada':
            raise ErrorOperacionNoPermitida("La reserva ya está cancelada")
        if self.estado_reserva == 'completada':
            raise ErrorOperacionNoPermitida("No se puede cancelar una reserva completada")
        self.estado_reserva = 'cancelada'
        self.costo_total = 0.0

    def obtener_descripcion(self) -> str:
        return (
            f"Reserva: {self._id} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion}h | "
            f"Estado: {self.estado_reserva} | Costo: ${self.costo_total:,.2f}"
        )

    def serializar(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'cliente_id': self.cliente.obtener_id(),
            'cliente_nombre': self.cliente.nombre,
            'servicio_id': self.servicio.obtener_id(),
            'servicio_nombre': self.servicio.nombre,
            'duracion': self.duracion,
            'costo_total': self.costo_total,
            'estado_reserva': self.estado_reserva,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_creacion': self._fecha_creacion.isoformat(),
        }