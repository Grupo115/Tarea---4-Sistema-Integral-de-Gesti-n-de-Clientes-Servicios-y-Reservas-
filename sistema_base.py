"""
sistema_base.py — Módulo base del Sistema Integral de Gestión.

Contiene los tres pilares de la arquitectura del sistema:

    1. Excepciones personalizadas
       Jerarquía de errores específicos del dominio para un manejo
       granular y profesional de situaciones anómalas.

    2. Clase abstracta EntidadBase
       Contrato común que deben cumplir todas las entidades del sistema
       (Cliente, Servicio, Reserva). Garantiza una interfaz consistente
       e implementa encapsulación, validaciones y polimorfismo.

    3. GestorLogs (Singleton thread-safe)
       Registro global de eventos y errores en archivo de texto.
       Una única instancia vive durante toda la ejecución.

Uso básico:
    from sistema_base import EntidadBase, GestorLogs, ErrorValidacion

Desarrollador responsable: Líder del equipo
"""

# ===========================================================================
# SECCIÓN 1 — EXCEPCIONES PERSONALIZADAS
# ===========================================================================

class ErrorValidacion(Exception):
    """
    Excepción lanzada cuando falla la validación de datos.

    Se utiliza cuando:
    - Email con formato inválido
    - Teléfono con dígitos incorrectos
    - Parámetros requeridos faltantes o vacíos
    - Valores fuera del rango permitido

    Ejemplo:
        try:
            validar_email(email)
        except ValueError as e:
            raise ErrorValidacion(f"Email inválido: {email}") from e
    """
    pass


class ErrorServicioNoDisponible(Exception):
    """
    Excepción lanzada cuando un servicio no existe o no está disponible.

    Se utiliza cuando:
    - Servicio no encontrado por ID
    - Servicio desactivado
    - Servicio sin disponibilidad en la fecha solicitada

    Ejemplo:
        if servicio_id not in servicios_disponibles:
            raise ErrorServicioNoDisponible(f"Servicio {servicio_id} no disponible")
    """
    pass


class ErrorReservaInvalida(Exception):
    """
    Excepción lanzada cuando los parámetros de una reserva son inválidos.

    Se utiliza cuando:
    - Cliente no registrado en el sistema
    - Servicio incompatible con el tipo de reserva
    - Duración inválida (negativa o cero)
    - Fechas no disponibles

    Ejemplo:
        if cliente not in clientes_registrados:
            raise ErrorReservaInvalida(f"Cliente {cliente_id} no existe")
    """
    pass


class ErrorOperacionNoPermitida(Exception):
    """
    Excepción lanzada cuando se intenta una operación inválida para el estado actual.

    Se utiliza cuando:
    - Intentar cancelar una reserva ya cancelada
    - Intentar modificar una reserva completada
    - Intentar confirmar una reserva ya confirmada

    Ejemplo:
        if reserva.estado == "cancelada":
            raise ErrorOperacionNoPermitida(
                f"No se puede cancelar reserva en estado {reserva.estado}"
            )
    """
    pass


class ErrorSistema(Exception):
    """
    Excepción lanzada cuando ocurre un error interno del sistema.

    Se utiliza cuando:
    - Falla en el cálculo de costos
    - Inconsistencia en la lógica de negocio
    - Operación aritmética inesperada

    Ejemplo:
        try:
            costo = calcular_costo(duracion)
        except ValueError as original:
            raise ErrorSistema("Cálculo inconsistente") from original
    """
    pass


# ===========================================================================
# SECCIÓN 2 — CLASE ABSTRACTA EntidadBase
# ===========================================================================

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict


class EntidadBase(ABC):
    """
    Clase abstracta que representa una entidad genérica del sistema.

    Todas las clases del dominio (Cliente, Servicio, Reserva, etc.) deben
    heredar de esta clase para garantizar una interfaz consistente.

    Atributos encapsulados:
        _id (str)               : Identificador único (no puede estar vacío)
        _fecha_creacion (datetime): Fecha y hora de creación automática
        _estado (str)           : Estado actual ('activo' o 'inactivo')

    Métodos abstractos que DEBEN implementarse en las subclases:
        - validar()             : Valida la integridad de los datos
        - obtener_descripcion() : Retorna descripción legible
        - serializar()          : Retorna los datos como diccionario
    """

    # Estados válidos para cualquier entidad del sistema
    ESTADOS_VALIDOS = {'activo', 'inactivo'}

    def __init__(self, id_entidad: str, estado: str = 'activo'):
        """
        Inicializa una entidad base con validaciones.

        Args:
            id_entidad (str): Identificador único (no puede estar vacío)
            estado (str)    : Estado inicial. Por defecto 'activo'

        Raises:
            ErrorValidacion: Si el ID está vacío o el estado es inválido
        """
        try:
            if not id_entidad or not isinstance(id_entidad, str) or id_entidad.strip() == "":
                raise ErrorValidacion("El ID de la entidad no puede estar vacío")

            if estado not in self.ESTADOS_VALIDOS:
                raise ErrorValidacion(
                    f"Estado inválido '{estado}'. "
                    f"Estados válidos: {self.ESTADOS_VALIDOS}"
                )

            self._id = id_entidad.strip()
            self._fecha_creacion = datetime.now()
            self._estado = estado

        except ErrorValidacion:
            raise  # Re-lanzar excepciones de validación sin modificar
        except Exception as e:
            raise ErrorValidacion(f"Error al inicializar entidad: {str(e)}") from e

    # ── Métodos abstractos ──────────────────────────────────────────────────

    @abstractmethod
    def validar(self) -> bool:
        """
        Valida la integridad de los datos de la entidad.

        Debe ser implementado por todas las subclases para realizar
        validaciones específicas de negocio.

        Returns:
            bool: True si la validación es exitosa

        Raises:
            ErrorValidacion: Si alguna validación falla

        Ejemplo en subclase:
            def validar(self):
                if not self.email or '@' not in self.email:
                    raise ErrorValidacion("Email inválido")
                return True
        """
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """
        Retorna una descripción legible de la entidad.

        Returns:
            str: Descripción completa de la entidad

        Ejemplo en subclase:
            def obtener_descripcion(self):
                return f"Cliente: {self.nombre} ({self.email})"
        """
        pass

    @abstractmethod
    def serializar(self) -> Dict[str, Any]:
        """
        Retorna los datos de la entidad en formato diccionario.

        Útil para logs, reportes y transmisión de datos.

        Returns:
            Dict[str, Any]: Diccionario con los datos de la entidad

        Ejemplo en subclase:
            def serializar(self):
                return {
                    'id': self._id,
                    'nombre': self.nombre,
                    'fecha_creacion': self._fecha_creacion.isoformat(),
                    'estado': self._estado
                }
        """
        pass

    # ── Métodos concretos ───────────────────────────────────────────────────

    def obtener_id(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self._id

    def obtener_estado(self) -> str:
        """Retorna el estado actual ('activo' o 'inactivo')."""
        return self._estado

    def obtener_fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora de creación de la entidad."""
        return self._fecha_creacion

    def cambiar_estado(self, nuevo_estado: str) -> None:
        """
        Cambia el estado de la entidad a uno válido.

        Args:
            nuevo_estado (str): Nuevo estado ('activo' o 'inactivo')

        Raises:
            ErrorValidacion: Si el nuevo estado no es válido
        """
        try:
            if nuevo_estado not in self.ESTADOS_VALIDOS:
                raise ErrorValidacion(
                    f"Estado inválido '{nuevo_estado}'. "
                    f"Estados válidos: {self.ESTADOS_VALIDOS}"
                )
            self._estado = nuevo_estado
        except ErrorValidacion:
            raise
        except Exception as e:
            raise ErrorValidacion(f"Error al cambiar estado: {str(e)}") from e

    def esta_activa(self) -> bool:
        """Retorna True si la entidad está activa."""
        return self._estado == 'activo'

    def __str__(self) -> str:
        """Representación legible de la entidad."""
        try:
            return self.obtener_descripcion()
        except Exception:
            return f"EntidadBase(id={self._id}, estado={self._estado})"

    def __repr__(self) -> str:
        """Representación técnica de la entidad."""
        return (
            f"{self.__class__.__name__}("
            f"id={self._id}, "
            f"estado={self._estado}, "
            f"fecha_creacion={self._fecha_creacion.isoformat()})"
        )

    def __eq__(self, otro) -> bool:
        """Dos entidades son iguales si comparten el mismo ID."""
        if not isinstance(otro, EntidadBase):
            return False
        return self._id == otro._id

    def __hash__(self) -> int:
        """Permite usar la entidad como clave en diccionarios/sets."""
        return hash(self._id)


# ===========================================================================
# SECCIÓN 3 — GESTOR DE LOGS (Singleton thread-safe)
# ===========================================================================

import os
import threading
from pathlib import Path
from typing import Optional


class GestorLogs:
    """
    Gestor de logs singleton que registra eventos y errores del sistema.

    Características:
        - Patrón Singleton: una única instancia en toda la aplicación
        - Thread-safe: usa locks para evitar condiciones de carrera
        - Registro comprensivo: eventos + errores con timestamps
        - Gestión automática de directorios

    Uso:
        from sistema_base import GestorLogs

        logger = GestorLogs()
        logger.registrar_evento("OPERACION", "Iniciando operación 1")
        try:
            operacion_con_riesgo()
        except Exception as e:
            logger.registrar_error(e, "ContextoOperacion")
    """

    _instancia = None          # Instancia única (Singleton)
    _lock = threading.Lock()   # Lock para creación thread-safe

    def __new__(cls):
        """Crea una única instancia del GestorLogs (patrón Singleton)."""
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:   # Double-checked locking
                    cls._instancia = super().__new__(cls)
                    cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        """Inicializa rutas y lock de escritura."""
        # La carpeta logs/ queda al mismo nivel que sistema_base.py
        self._carpeta_logs = Path(__file__).parent / "logs"
        self._archivo_log = self._carpeta_logs / "eventos.log"

        try:
            self._carpeta_logs.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"[ERROR] No se pudo crear carpeta de logs: {e}")
            self._carpeta_logs = Path.cwd() / "logs"
            self._carpeta_logs.mkdir(parents=True, exist_ok=True)
            self._archivo_log = self._carpeta_logs / "eventos.log"

        self._lock_escritura = threading.Lock()

    # ── Métodos públicos ────────────────────────────────────────────────────

    def registrar_evento(self, tipo_evento: str, mensaje: str, contexto: str = "") -> None:
        """
        Registra un evento informativo en el archivo de logs.

        Args:
            tipo_evento (str): Categoría del evento (EXITO, INICIO, FIN, etc.)
            mensaje (str)    : Descripción del evento
            contexto (str)   : Contexto adicional opcional (ej. "Op1")

        Ejemplo:
            logger.registrar_evento("EXITO", "Cliente creado", "Op1")
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if contexto:
                linea = f"[{timestamp}] [{tipo_evento}] [{contexto}] {mensaje}\n"
            else:
                linea = f"[{timestamp}] [{tipo_evento}] {mensaje}\n"

            with self._lock_escritura:
                with open(self._archivo_log, 'a', encoding='utf-8') as f:
                    f.write(linea)
        except Exception as e:
            print(f"[ERROR CRÍTICO] No se pudo escribir en log: {e}")

    def registrar_error(self, excepcion: Exception, contexto: str = "") -> None:
        """
        Registra una excepción/error en el archivo de logs.

        Args:
            excepcion (Exception): La excepción a registrar
            contexto (str)       : Contexto donde ocurrió el error

        Ejemplo:
            try:
                validar_email(email)
            except ErrorValidacion as e:
                logger.registrar_error(e, "ValidacionCliente")
        """
        try:
            nombre = excepcion.__class__.__name__
            mensaje = str(excepcion)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if contexto:
                linea = f"[{timestamp}] [ERROR] [{contexto}] {nombre}: {mensaje}\n"
            else:
                linea = f"[{timestamp}] [ERROR] {nombre}: {mensaje}\n"

            with self._lock_escritura:
                with open(self._archivo_log, 'a', encoding='utf-8') as f:
                    f.write(linea)
        except Exception as e:
            print(f"[ERROR CRÍTICO] No se pudo registrar error: {e}")

    def registrar_operacion(self, numero: int, descripcion: str) -> None:
        """
        Registra el inicio de una operación numerada.

        Args:
            numero (int)       : Número secuencial de la operación
            descripcion (str)  : Qué hace la operación
        """
        self.registrar_evento("OPERACION", f"Op{numero}: {descripcion}")

    def limpiar_logs(self) -> None:
        """
        Vacía el archivo de logs.

        Útil al inicio de cada sesión de pruebas.
        NOTA: El lock se libera antes de llamar a registrar_evento
        para evitar un deadlock (threading.Lock no es reentrante).
        """
        try:
            with self._lock_escritura:
                if self._archivo_log.exists():
                    with open(self._archivo_log, 'w', encoding='utf-8') as f:
                        f.write("")
            # Fuera del with para no re-adquirir el lock
            self.registrar_evento("SISTEMA", "Logs limpiados")
        except Exception as e:
            print(f"[ERROR] No se pudo limpiar logs: {e}")

    def obtener_ruta_archivo(self) -> Path:
        """Retorna la ruta completa al archivo eventos.log."""
        return self._archivo_log

    def obtener_logs(self) -> str:
        """Retorna el contenido actual del archivo de logs como string."""
        try:
            if self._archivo_log.exists():
                with open(self._archivo_log, 'r', encoding='utf-8') as f:
                    return f.read()
            return "[No hay logs disponibles]"
        except Exception as e:
            return f"[ERROR al leer logs: {e}]"


# ===========================================================================
# Exportaciones explícitas del módulo
# ===========================================================================

__all__ = [
    # Excepciones
    "ErrorValidacion",
    "ErrorServicioNoDisponible",
    "ErrorReservaInvalida",
    "ErrorOperacionNoPermitida",
    "ErrorSistema",
    # Clase abstracta
    "EntidadBase",
    # Gestor de logs
    "GestorLogs",
]
