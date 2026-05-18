"""
clases_demo.py — Stubs temporales para pruebas del simulador.

ADVERTENCIA: Este archivo es un PLACEHOLDER para uso exclusivo del simulador
mientras los demás integrantes del equipo no hayan subido sus módulos reales.

Cuando el equipo integre:
  - clientes/cliente.py      → reemplazar importación en simulador.py
  - servicios/servicio.py    → reemplazar importación en simulador.py
  - reservas/reserva.py      → reemplazar importación en simulador.py

NO modificar este archivo en la integración final. Solo actualizar las
importaciones en simulador.py.
"""

# import re
# from datetime import datetime
# from typing import Dict, Any
# 
# from sistema_base import (
#     EntidadBase,
#     ErrorValidacion,
#     ErrorReservaInvalida,
#     ErrorOperacionNoPermitida,
#     ErrorSistema,
# )


# class ClienteDemo(EntidadBase):
#     """
#     Stub de Cliente para demostración del simulador.
#     Será reemplazado por la clase real del compañero encargado de clientes.
#     """
# 
#     def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
#         super().__init__(id_cliente)
#         self.nombre = nombre
#         self.email = email
#         self.telefono = telefono
#         self.validar()
# 
#     def validar(self) -> bool:
#         if not self.nombre or len(self.nombre.strip()) < 3:
#             raise ErrorValidacion("Nombre debe tener al menos 3 caracteres")
# 
#         patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#         if not re.match(patron_email, self.email):
#             raise ErrorValidacion(f"Email inválido: {self.email}")
# 
#         if not re.match(r'^\d{10}$', self.telefono):
#             raise ErrorValidacion(
#                 f"Teléfono debe tener exactamente 10 dígitos: {self.telefono}"
#             )
#         return True
# 
#     def obtener_descripcion(self) -> str:
#         return f"Cliente: {self.nombre} ({self.email}) - Tel: {self.telefono}"
# 
#     def serializar(self) -> Dict[str, Any]:
#         return {
#             'id': self._id,
#             'nombre': self.nombre,
#             'email': self.email,
#             'telefono': self.telefono,
#             'estado': self._estado,
#             'fecha_creacion': self._fecha_creacion.isoformat(),
#         }


# class ServicioDemo(EntidadBase):
#     """
#     Stub de Servicio para demostración del simulador.
#     Será reemplazado por la clase real del compañero encargado de servicios.
#     """
# 
#     TIPOS_VALIDOS = {'reserva_sala', 'alquiler_equipo', 'asesoria'}
# 
#     def __init__(self, id_servicio: str, nombre: str, precio_base: float, tipo: str):
#         super().__init__(id_servicio)
#         self.nombre = nombre
#         self.precio_base = precio_base
#         self.tipo = tipo
#         self.validar()
# 
#     def validar(self) -> bool:
#         if not self.nombre or len(self.nombre.strip()) < 3:
#             raise ErrorValidacion("Nombre del servicio debe tener al menos 3 caracteres")
#         if self.precio_base <= 0:
#             raise ErrorValidacion(f"Precio base debe ser positivo: {self.precio_base}")
#         if self.tipo not in self.TIPOS_VALIDOS:
#             raise ErrorValidacion(f"Tipo de servicio inválido: {self.tipo}")
#         return True
# 
#     def calcular_costo(self, duracion: float, **kwargs) -> float:
#         """
#         Calcula el costo del servicio (método con parámetros opcionales).
# 
#         Args:
#             duracion (float): Duración del servicio
#             descuento (float): Porcentaje de descuento (0-1). Por defecto 0.
#             impuesto (bool): Aplicar IVA del 19%. Por defecto False.
#         """
#         descuento = kwargs.get('descuento', 0)
#         aplicar_impuesto = kwargs.get('impuesto', False)
# 
#         try:
#             if duracion <= 0:
#                 raise ValueError(f"Duración debe ser positiva: {duracion}")
# 
#             costo = self.precio_base * duracion
# 
#             if descuento > 0:
#                 costo *= (1 - descuento)
# 
#             if aplicar_impuesto:
#                 costo *= 1.19
# 
#             return costo
#         except ValueError as e:
#             raise ErrorSistema(f"Cálculo inconsistente: {str(e)}") from e
# 
#     def obtener_descripcion(self) -> str:
#         return f"Servicio: {self.nombre} ({self.tipo}) - ${self.precio_base:,.0f}/unidad"
# 
#     def serializar(self) -> Dict[str, Any]:
#         return {
#             'id': self._id,
#             'nombre': self.nombre,
#             'tipo': self.tipo,
#             'precio_base': self.precio_base,
#             'estado': self._estado,
#             'fecha_creacion': self._fecha_creacion.isoformat(),
#         }


# class ReservaDemo(EntidadBase):
#     """
#     Stub de Reserva para demostración del simulador.
#     Será reemplazado por la clase real del compañero encargado de reservas.
#     """
# 
#     ESTADOS_RESERVA = {'pendiente', 'confirmada', 'cancelada', 'completada'}
# 
#     def __init__(
#         self,
#         id_reserva: str,
#         cliente: ClienteDemo,
#         servicio: ServicioDemo,
#         duracion: float,
#         fecha_inicio: datetime,
#     ):
#         super().__init__(id_reserva, estado='activo')
#         self.cliente = cliente
#         self.servicio = servicio
#         self.duracion = duracion
#         self.fecha_inicio = fecha_inicio
#         self.costo_total = 0.0
#         self.estado_reserva = 'pendiente'
#         self.validar()
# 
#     def validar(self) -> bool:
#         if not isinstance(self.cliente, ClienteDemo):
#             raise ErrorReservaInvalida("Cliente debe ser un objeto Cliente")
#         if not isinstance(self.servicio, ServicioDemo):
#             raise ErrorReservaInvalida("Servicio debe ser un objeto Servicio")
#         if self.duracion <= 0:
#             raise ErrorReservaInvalida(f"Duración debe ser positiva: {self.duracion}")
#         if not isinstance(self.fecha_inicio, datetime):
#             raise ErrorReservaInvalida("Fecha de inicio debe ser un datetime")
#         return True
# 
#     def confirmar(self) -> None:
#         if self.estado_reserva == 'confirmada':
#             raise ErrorOperacionNoPermitida("La reserva ya está confirmada")
#         if self.estado_reserva == 'cancelada':
#             raise ErrorOperacionNoPermitida("No se puede confirmar una reserva cancelada")
#         self.costo_total = self.servicio.calcular_costo(self.duracion)
#         self.estado_reserva = 'confirmada'
# 
#     def cancelar(self) -> None:
#         if self.estado_reserva == 'cancelada':
#             raise ErrorOperacionNoPermitida("La reserva ya está cancelada")
#         if self.estado_reserva == 'completada':
#             raise ErrorOperacionNoPermitida("No se puede cancelar una reserva completada")
#         self.estado_reserva = 'cancelada'
#         self.costo_total = 0.0
# 
#     def obtener_descripcion(self) -> str:
#         return (
#             f"Reserva: {self._id} | Cliente: {self.cliente.nombre} | "
#             f"Servicio: {self.servicio.nombre} | Duración: {self.duracion}h | "
#             f"Estado: {self.estado_reserva} | Costo: ${self.costo_total:,.2f}"
#         )
# 
#     def serializar(self) -> Dict[str, Any]:
#         return {
#             'id': self._id,
#             'cliente_id': self.cliente._id,
#             'cliente_nombre': self.cliente.nombre,
#             'servicio_id': self.servicio._id,
#             'servicio_nombre': self.servicio.nombre,
#             'duracion': self.duracion,
#             'costo_total': self.costo_total,
#             'estado_reserva': self.estado_reserva,
#             'fecha_inicio': self.fecha_inicio.isoformat(),
#             'fecha_creacion': self._fecha_creacion.isoformat(),
#         }
