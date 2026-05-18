"""
Módulo simulador: Ejecuta 10 operaciones demostrando manejo robusto de excepciones.

Este módulo simula operaciones completas del sistema de gestión con:
- Creación de clientes (válida e inválida)
- Creación de servicios (válida e inválida)
- Creación y gestión de reservas (válidas e inválidas)
- Cálculos con encadenamiento de excepciones

Cada operación usa bloques try/except/else/finally para demostrar
manejo profesional de errores.

Integración con módulos del equipo:
    Cuando los compañeros suban sus módulos reales, reemplazar las
    importaciones de clases_demo por los módulos correspondientes:

        from clientes.cliente import Cliente
        from servicios.servicio import Servicio
        from reservas.reserva import Reserva
"""

from sistema_base import (
    GestorLogs,
    ErrorValidacion,
    ErrorServicioNoDisponible,
    ErrorReservaInvalida,
    ErrorOperacionNoPermitida,
    ErrorSistema,
)
# ─── Importar clases del equipo ───────────────────────────────────────────────

from Cliente import Cliente
from servicio import crear_servicio as Servicio
from Reserva import Reserva
# ─────────────────────────────────────────────────────────────────────────────
from datetime import datetime
from typing import Dict, Any, List, Optional


# ============================================================================
# CONTENEDORES GLOBALES PARA ALMACENAMIENTO EN MEMORIA
# ============================================================================

clientes: Dict[str, Cliente] = {}
servicios: Dict[str, Servicio] = {}
reservas: Dict[str, Reserva] = {}


# ============================================================================
# FUNCIONES DE OPERACIONES
# ============================================================================

def operacion_1(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 1 (VÁLIDA): Crear cliente con datos correctos.
    
    Demuestra:
    - Creación exitosa de un Cliente
    - Bloque try/except/else/finally
    - Almacenamiento en memoria
    - Registro de evento exitoso
    
    Returns:
        bool: True si la operación fue exitosa
    """
    print("\n" + "="*70)
    print("OPERACIÓN 1: Crear cliente válido (Juan Pérez)")
    print("="*70)
    
    try:
        logger.registrar_operacion(1, "Crear cliente válido")
        
        # Crear cliente con datos válidos
        cliente = Cliente(
            id_cliente="CLI001",
            nombre="Juan Pérez García",
            email="juan.perez@email.com",
            telefono="3201234567"
        )
        
        # Almacenar en memoria
        clientes["CLI001"] = cliente
        
    except ErrorValidacion as e:
        # Capturar errores de validación
        logger.registrar_error(e, "Op1-ValidacionCliente")
        print(f"[OP 1] ❌ Error de validación: {e}")
        return False
    
    except Exception as e:
        # Capturar cualquier otra excepción inesperada
        logger.registrar_error(e, "Op1-Inesperado")
        print(f"[OP 1] ❌ Error inesperado: {e}")
        return False
    
    else:
        # Se ejecuta solo si NO hubo excepción
        print(f"[OP 1] ✅ Cliente creado correctamente: {cliente.obtener_descripcion()}")
        logger.registrar_evento("EXITO", "Cliente creado correctamente", "Op1")
        return True
    
    finally:
        # Siempre se ejecuta
        print("[OP 1] Finalizando operación...")


def operacion_2(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 2 (INVÁLIDA): Intentar crear cliente con email inválido.
    
    Demuestra:
    - Manejo de ErrorValidacion
    - Captura controlada de excepciones
    - Continuación del programa tras error
    - Sistema sigue funcionando
    
    Returns:
        bool: False (operación fallida como se espera)
    """
    print("\n" + "="*70)
    print("OPERACIÓN 2: Intentar crear cliente con email inválido")
    print("="*70)
    
    try:
        logger.registrar_operacion(2, "Crear cliente con email inválido")
        
        # Intentar crear cliente con email malformado
        cliente = Cliente(
            id_cliente="CLI002",
            nombre="María López",
            email="maria.lopez@",  # Email inválido (falta dominio)
            telefono="3209876543"
        )
        
    except ErrorValidacion as e:
        # Capturar validación
        logger.registrar_error(e, "Op2-EmailInvalido")
        print(f"[OP 2] ⚠️  Error capturado: {e}")
        logger.registrar_evento("INTENTO_FALLIDO", "Email inválido", "Op2")
        return False
    
    except Exception as e:
        # Otras excepciones
        logger.registrar_error(e, "Op2-Inesperado")
        print(f"[OP 2] ❌ Error inesperado: {e}")
        return False
    
    else:
        # No debería ejecutarse en este caso
        print("[OP 2] ✅ Cliente creado (inesperado)")
        return True
    
    finally:
        print("[OP 2] Finalizando operación...")


def operacion_3(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 3 (VÁLIDA): Crear servicio válido (Reserva de Sala).
    
    Demuestra:
    - Creación de Servicio exitosa
    - Almacenamiento en memoria
    - Diferentes tipos de servicios
    
    Returns:
        bool: True si la operación fue exitosa
    """
    print("\n" + "="*70)
    print("OPERACIÓN 3: Crear servicio válido (Reserva de Sala)")
    print("="*70)
    
    try:
        logger.registrar_operacion(3, "Crear servicio de reserva de sala")
        
        # Crear servicio con parámetros válidos
        servicio = Servicio(
            id_servicio="SERV001",
            nombre="Sala de Conferencias Premium",
            precio_base=150000.0,
            tipo="reserva_sala"
        )
        
        # Almacenar en memoria
        servicios["SERV001"] = servicio
        
    except ErrorValidacion as e:
        logger.registrar_error(e, "Op3-ValidacionServicio")
        print(f"[OP 3] ❌ Error: {e}")
        return False
    
    except Exception as e:
        logger.registrar_error(e, "Op3-Inesperado")
        print(f"[OP 3] ❌ Error inesperado: {e}")
        return False
    
    else:
        print(f"[OP 3] ✅ Servicio creado: {servicio.obtener_descripcion()}")
        logger.registrar_evento("EXITO", "Servicio creado correctamente", "Op3")
        return True
    
    finally:
        print("[OP 3] Finalizando operación...")


def operacion_4(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 4 (INVÁLIDA): Crear servicio con precio negativo.
    
    Demuestra:
    - Validación de parámetros numéricos
    - Captura de ErrorValidacion
    - Manejo controlado de datos inválidos
    
    Returns:
        bool: False (fallida como se espera)
    """
    print("\n" + "="*70)
    print("OPERACIÓN 4: Intentar crear servicio con precio negativo")
    print("="*70)
    
    try:
        logger.registrar_operacion(4, "Crear servicio con precio inválido")
        
        # Intentar crear servicio con precio negativo
        servicio = Servicio(
            id_servicio="SERV002",
            nombre="Equipo de Audiovisual",
            precio_base=-50000.0,  # Precio negativo (inválido)
            tipo="alquiler_equipo"
        )
        
    except ErrorValidacion as e:
        logger.registrar_error(e, "Op4-PrecioNegativo")
        print(f"[OP 4] ⚠️  Error capturado: {e}")
        logger.registrar_evento("INTENTO_FALLIDO", "Precio negativo", "Op4")
        return False
    
    except Exception as e:
        logger.registrar_error(e, "Op4-Inesperado")
        print(f"[OP 4] ❌ Error inesperado: {e}")
        return False
    
    else:
        print("[OP 4] ✅ Servicio creado (inesperado)")
        return True
    
    finally:
        print("[OP 4] Finalizando operación...")


def operacion_5(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 5 (VÁLIDA): Crear reserva válida, confirmarla y calcular costo.
    
    Demuestra:
    - Creación de Reserva
    - Confirmación de reserva
    - Cálculo de costo
    - Encadenamiento de operaciones exitosas
    
    Returns:
        bool: True si la operación fue exitosa
    """
    print("\n" + "="*70)
    print("OPERACIÓN 5: Crear reserva válida, confirmar y calcular costo")
    print("="*70)
    
    try:
        logger.registrar_operacion(5, "Crear y confirmar reserva válida")
        
        # Crear reserva con datos válidos
        reserva = Reserva(
            id_reserva="RES001",
            cliente=clientes["CLI001"],  # Usar cliente de Op1
            servicio=servicios["SERV001"],  # Usar servicio de Op3
            duracion=2.5,  # 2.5 horas
            fecha_inicio=datetime.now()
        )
        
        # Confirmar la reserva
        reserva.confirmar()
        
        # Almacenar en memoria
        reservas["RES001"] = reserva
        
    except ErrorReservaInvalida as e:
        logger.registrar_error(e, "Op5-ParametrosReserva")
        print(f"[OP 5] ❌ Error en reserva: {e}")
        return False
    
    except Exception as e:
        logger.registrar_error(e, "Op5-Inesperado")
        print(f"[OP 5] ❌ Error inesperado: {e}")
        return False
    
    else:
        print(f"[OP 5] ✅ Reserva creada y confirmada: {reserva.obtener_descripcion()}")
        logger.registrar_evento("EXITO", "Reserva confirmada con éxito", "Op5")
        return True
    
    finally:
        print("[OP 5] Finalizando operación...")


def operacion_6(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 6 (INVÁLIDA): Intentar crear reserva con cliente inexistente.
    
    Demuestra:
    - Validación de referencias (cliente debe existir)
    - ErrorReservaInvalida
    - Validación antes de crear objeto
    
    Returns:
        bool: False (fallida como se espera)
    """
    print("\n" + "="*70)
    print("OPERACIÓN 6: Intentar crear reserva con cliente inexistente")
    print("="*70)
    
    try:
        logger.registrar_operacion(6, "Crear reserva con cliente inexistente")
        
        # Crear cliente ficticio que no está en el sistema
        cliente_fantasma = Cliente(
            id_cliente="CLI_FAKE",
            nombre="Cliente Inexistente",
            email="fake@email.com",
            telefono="1234567890"
        )
        
        # Intentar crear reserva (cliente_fantasma no está en clientes{})
        if "CLI_FAKE" not in clientes:
            raise ErrorReservaInvalida("El cliente no está registrado en el sistema")
        
        reserva = Reserva(
            id_reserva="RES002",
            cliente=cliente_fantasma,
            servicio=servicios["SERV001"],
            duracion=1.0,
            fecha_inicio=datetime.now()
        )
        
    except ErrorReservaInvalida as e:
        logger.registrar_error(e, "Op6-ClienteNoExiste")
        print(f"[OP 6] ⚠️  Error capturado: {e}")
        logger.registrar_evento("INTENTO_FALLIDO", "Cliente no registrado", "Op6")
        return False
    
    except Exception as e:
        logger.registrar_error(e, "Op6-Inesperado")
        print(f"[OP 6] ❌ Error inesperado: {e}")
        return False
    
    else:
        print("[OP 6] ✅ Reserva creada (inesperado)")
        return True
    
    finally:
        print("[OP 6] Finalizando operación...")


def operacion_7(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 7 (VÁLIDA): Cancelar una reserva confirmada.
    
    Demuestra:
    - Cambio de estado de reserva (confirmada -> cancelada)
    - Operación permitida en estado válido
    - Costo vuelve a 0 al cancelar
    
    Returns:
        bool: True si la operación fue exitosa
    """
    print("\n" + "="*70)
    print("OPERACIÓN 7: Cancelar reserva confirmada")
    print("="*70)
    
    try:
        logger.registrar_operacion(7, "Cancelar reserva confirmada")
        
        # Usar reserva creada en Op5
        reserva = reservas["RES001"]
        
        # Verificar que está confirmada antes de cancelar
        if reserva.estado_reserva != 'confirmada':
            raise ErrorOperacionNoPermitida(f"Reserva en estado {reserva.estado_reserva}")
        
        # Cancelar
        reserva.cancelar()
        
    except ErrorOperacionNoPermitida as e:
        logger.registrar_error(e, "Op7-EstadoInvalido")
        print(f"[OP 7] ⚠️  Error: {e}")
        return False
    
    except Exception as e:
        logger.registrar_error(e, "Op7-Inesperado")
        print(f"[OP 7] ❌ Error inesperado: {e}")
        return False
    
    else:
        print(f"[OP 7] ✅ Reserva cancelada: {reserva.obtener_descripcion()}")
        logger.registrar_evento("EXITO", "Reserva cancelada correctamente", "Op7")
        return True
    
    finally:
        print("[OP 7] Finalizando operación...")


def operacion_8(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 8 (INVÁLIDA): Intentar cancelar una reserva ya cancelada.
    
    Demuestra:
    - ErrorOperacionNoPermitida
    - Validación de estado actual
    - Transiciones inválidas entre estados
    
    Returns:
        bool: False (fallida como se espera)
    """
    print("\n" + "="*70)
    print("OPERACIÓN 8: Intentar cancelar reserva ya cancelada")
    print("="*70)
    
    try:
        logger.registrar_operacion(8, "Cancelar reserva ya cancelada")
        
        # Usar reserva de Op7 (ya está cancelada)
        reserva = reservas["RES001"]
        
        # Intentar cancelar nuevamente
        reserva.cancelar()
        
    except ErrorOperacionNoPermitida as e:
        logger.registrar_error(e, "Op8-ReservaCancelada")
        print(f"[OP 8] ⚠️  Error capturado: {e}")
        logger.registrar_evento("INTENTO_FALLIDO", "Reserva ya cancelada", "Op8")
        return False
    
    except Exception as e:
        logger.registrar_error(e, "Op8-Inesperado")
        print(f"[OP 8] ❌ Error inesperado: {e}")
        return False
    
    else:
        print("[OP 8] ✅ Reserva cancelada (inesperado)")
        return True
    
    finally:
        print("[OP 8] Finalizando operación...")


def operacion_9(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 9 (VÁLIDA): Calcular costo con descuento (método sobrecargado).
    
    Demuestra:
    - Método sobrecargado: calcular_costo() con parámetros opcionales
    - Cálculo con descuento
    - Bloque else ejecutándose en operación exitosa
    
    Returns:
        bool: True si la operación fue exitosa
    """
    print("\n" + "="*70)
    print("OPERACIÓN 9: Calcular costo con descuento (método sobrecargado)")
    print("="*70)
    
    try:
        logger.registrar_operacion(9, "Calcular costo con descuento")
        
        # Usar servicio de Op3
        servicio = servicios["SERV001"]
        
        # Método sobrecargado: calcular_costo(duracion, descuento=0.1)
        duracion = 3.0
        descuento = 0.15  # 15% de descuento
        costo_con_descuento = servicio.calcular_costo(
            duracion,
            descuento=descuento
        )
        
        # Verificar resultado
        costo_base = servicio.precio_base * duracion
        costo_esperado = costo_base * (1 - descuento)
        
        if abs(costo_con_descuento - costo_esperado) < 0.01:
            resultado_valid = True
        else:
            raise ErrorSistema("Cálculo de descuento inconsistente")
        
    except ErrorSistema as e:
        logger.registrar_error(e, "Op9-CalculoIncorrecto")
        print(f"[OP 9] ❌ Error en cálculo: {e}")
        return False
    
    except Exception as e:
        logger.registrar_error(e, "Op9-Inesperado")
        print(f"[OP 9] ❌ Error inesperado: {e}")
        return False
    
    else:
        print(f"[OP 9] ✅ Cálculo con descuento: ${costo_con_descuento:,.2f}")
        print(f"       (Base: ${costo_base:,.2f} - Descuento 15%: ${costo_base*0.15:,.2f})")
        logger.registrar_evento("EXITO", f"Cálculo con descuento exitoso: ${costo_con_descuento:,.2f}", "Op9")
        return True
    
    finally:
        print("[OP 9] Finalizando operación...")


def operacion_10(logger: GestorLogs) -> bool:
    """
    OPERACIÓN 10 (INVÁLIDA): Calcular costo con parámetro inválido + encadenamiento.
    
    Demuestra:
    - Encadenamiento de excepciones: raise ... from original_error
    - Conversión de ValueError a ErrorSistema
    - Captura de excepción encadenada
    - Información completa de debugging
    
    Returns:
        bool: False (fallida como se espera)
    """
    print("\n" + "="*70)
    print("OPERACIÓN 10: Calcular costo con parámetro inválido (encadenamiento)")
    print("="*70)
    
    try:
        logger.registrar_operacion(10, "Calcular costo con duración negativa")
        
        servicio = servicios["SERV001"]
        duracion_invalida = -5.0  # Duración negativa (inválida)
        
        # Esto generará ValueError en calcular_costo, que será
        # encadenado a ErrorSistema
        try:
            costo = servicio.calcular_costo(duracion_invalida)
        except ErrorSistema as e:
            # ErrorSistema contiene referencia a ValueError original
            print(f"[OP 10] Excepción encadenada capturada:")
            print(f"        - Excepción actual: {e.__class__.__name__}: {e}")
            print(f"        - Causa original: {e.__cause__.__class__.__name__}: {e.__cause__}")
            raise  # Re-lanzar para capturarlo en except exterior
        
    except ErrorSistema as e:
        logger.registrar_error(e, "Op10-DuracionNegativa")
        print(f"[OP 10] ⚠️  Error capturado (encadenado): {e}")
        if e.__cause__:
            print(f"[OP 10] Causa original: {e.__cause__}")
        logger.registrar_evento("INTENTO_FALLIDO", "Duración negativa - encadenamiento", "Op10")
        return False
    
    except Exception as e:
        logger.registrar_error(e, "Op10-Inesperado")
        print(f"[OP 10] ❌ Error inesperado: {e}")
        return False
    
    else:
        print("[OP 10] ✅ Cálculo exitoso (inesperado)")
        return True
    
    finally:
        print("[OP 10] Finalizando operación...")


# ============================================================================
# FUNCIÓN MAIN
# ============================================================================

def main():
    """
    Ejecuta las 10 operaciones del sistema de manera secuencial.
    
    Demuestra:
    - Manejo integral de excepciones
    - Try/except/else/finally en cada operación
    - Sistema funcionando continuamente (no se detiene por errores)
    - Registro completo en logs
    - Resumen final de resultados
    """
    
    print("\n" + "="*70)
    print(" SISTEMA INTEGRAL DE GESTIÓN - SIMULACIÓN DE 10 OPERACIONES")
    print("="*70)
    print("Desarrollador Líder: Sebas")
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Obtener instancia única del logger (Singleton)
    logger = GestorLogs()
    
    # Limpiar logs anteriores (opcional)
    logger.limpiar_logs()
    
    logger.registrar_evento(
        "INICIO_SISTEMA",
        "Iniciando simulación de 10 operaciones",
        "MAIN"
    )
    
    # Lista para tracking de resultados
    resultados = []
    
    try:
        # =====================================================================
        # BLOQUE TRY: Ejecutar todas las operaciones
        # =====================================================================
        
        # Operación 1 (válida)
        resultado = operacion_1(logger)
        resultados.append(("Op 1", resultado, "Crear cliente válido"))
        
        # Operación 2 (inválida)
        resultado = operacion_2(logger)
        resultados.append(("Op 2", resultado, "Cliente con email inválido"))
        
        # Operación 3 (válida)
        resultado = operacion_3(logger)
        resultados.append(("Op 3", resultado, "Crear servicio válido"))
        
        # Operación 4 (inválida)
        resultado = operacion_4(logger)
        resultados.append(("Op 4", resultado, "Servicio con precio negativo"))
        
        # Operación 5 (válida)
        resultado = operacion_5(logger)
        resultados.append(("Op 5", resultado, "Crear y confirmar reserva"))
        
        # Operación 6 (inválida)
        resultado = operacion_6(logger)
        resultados.append(("Op 6", resultado, "Reserva con cliente inexistente"))
        
        # Operación 7 (válida)
        resultado = operacion_7(logger)
        resultados.append(("Op 7", resultado, "Cancelar reserva confirmada"))
        
        # Operación 8 (inválida)
        resultado = operacion_8(logger)
        resultados.append(("Op 8", resultado, "Cancelar reserva ya cancelada"))
        
        # Operación 9 (válida)
        resultado = operacion_9(logger)
        resultados.append(("Op 9", resultado, "Calcular costo con descuento"))
        
        # Operación 10 (inválida con encadenamiento)
        resultado = operacion_10(logger)
        resultados.append(("Op 10", resultado, "Cálculo con encadenamiento de excepciones"))
        
    except Exception as e:
        # =====================================================================
        # BLOQUE EXCEPT: Capturar cualquier excepción no manejada
        # =====================================================================
        print(f"\n[MAIN] ❌ ERROR CRÍTICO NO CONTROLADO: {e}")
        logger.registrar_error(e, "MAIN-ErrorCritico")
        raise  # Re-lanzar si es realmente crítico
    
    else:
        # =====================================================================
        # BLOQUE ELSE: Se ejecuta si NO hubo excepciones en el try
        # =====================================================================
        print("\n" + "="*70)
        print("✅ TODAS LAS OPERACIONES EJECUTADAS SIN INTERRUPCIONES")
        print("="*70)
        logger.registrar_evento("EXITO", "Todas las operaciones completadas sin crashes", "MAIN")
    
    finally:
        # =====================================================================
        # BLOQUE FINALLY: Siempre se ejecuta (cleanup)
        # =====================================================================
        print("\n" + "="*70)
        print(" RESUMEN FINAL DE RESULTADOS")
        print("="*70)
        
        exitosas = sum(1 for _, resultado, _ in resultados if resultado)
        fallidas = len(resultados) - exitosas
        
        print(f"\nTotal de operaciones: {len(resultados)}")
        print(f"Exitosas: {exitosas} ✅")
        print(f"Fallidas: {fallidas} ❌")
        print(f"\nDetalles:")
        
        for op, resultado, descripcion in resultados:
            estado = "✅ ÉXITO" if resultado else "❌ FALLO (esperado)"
            print(f"  {op}: {estado:20} | {descripcion}")
        
        print("\n" + "="*70)
        print(" ARCHIVO DE LOGS")
        print("="*70)
        ruta_logs = logger.obtener_ruta_archivo()
        print(f"Ubicación: {ruta_logs}")
        print(f"\nContenido del archivo de logs:")
        print("-" * 70)
        
        contenido_logs = logger.obtener_logs()
        print(contenido_logs)
        
        print("-" * 70)
        print(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        print("\n✅ SIMULACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        
        logger.registrar_evento(
            "FIN_SISTEMA",
            f"Simulación completada: {exitosas} exitosas, {fallidas} fallidas",
            "MAIN"
        )


if __name__ == "__main__":
    main()
