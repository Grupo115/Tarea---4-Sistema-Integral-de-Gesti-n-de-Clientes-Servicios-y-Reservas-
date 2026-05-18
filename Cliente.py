# ==============================
# IMPORTACIONES DEL SISTEMA BASE
# ==============================

from sistema_base import EntidadBase, ErrorValidacion, GestorLogs
import re


# ==============================
# CLASE CLIENTE
# ==============================

class Cliente(EntidadBase):

    def __init__(self, id_cliente, nombre, email, telefono, estado="activo"):
        try:
            # Inicializar clase base (valida ID y estado)
            super().__init__(id_cliente, estado)

            # Encapsulación de atributos
            self._nombre = nombre.strip()
            self._email = email.strip().lower()
            self._telefono = telefono.strip()

            # Validación completa
            self.validar()

        except ErrorValidacion:
            raise  # Re-lanzar sin modificar

        except Exception as e:
            GestorLogs().registrar_error(e, "Cliente-Init")
            raise ErrorValidacion("Error al crear cliente") from e


    # ==============================
    # VALIDACIONES 
    # ==============================

    def validar(self):
        try:
            # -------- VALIDAR NOMBRE --------
            if not self._nombre:
                raise ErrorValidacion("El nombre no puede estar vacío")

            if len(self._nombre) < 3:
                raise ErrorValidacion("El nombre debe tener al menos 3 caracteres")

            # Permitir letras, espacios y tildes
            if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', self._nombre):
                raise ErrorValidacion("El nombre solo puede contener letras y espacios")

            # -------- VALIDAR EMAIL --------
            if not self._email:
                raise ErrorValidacion("El email no puede estar vacío")

            if len(self._email) < 6:
                raise ErrorValidacion("El email es demasiado corto")

            patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(patron_email, self._email):
                raise ErrorValidacion(f"Formato de email inválido: {self._email}")

            # -------- VALIDAR TELÉFONO --------
            if not self._telefono:
                raise ErrorValidacion("El teléfono no puede estar vacío")

            if not self._telefono.isdigit():
                raise ErrorValidacion("El teléfono solo debe contener números")

            if len(self._telefono) != 10:
                raise ErrorValidacion("El teléfono debe tener exactamente 10 dígitos")

            # -------- VALIDACIÓN DE ESTADO --------
            if not self.esta_activa():
                raise ErrorValidacion("El cliente no está activo")

            return True

        except ErrorValidacion:
            raise

        except Exception as e:
            raise ErrorValidacion("Error inesperado en validación de cliente") from e


    # ==============================
    # DESCRIPCIÓN LEGIBLE
    # ==============================

    def obtener_descripcion(self):
        try:
            return (
                f"Cliente: {self._nombre} | "
                f"Email: {self._email} | "
                f"Teléfono: {self._telefono} | "
                f"Estado: {self.obtener_estado()}"
            )
        except Exception as e:
            GestorLogs().registrar_error(e, "Cliente-Descripcion")
            return "Error al obtener descripción del cliente"


    # ==============================
    # SERIALIZACIÓN PARA LOGS / REPORTES
    # ==============================

    def serializar(self):
        try:
            return {
                "id": self.obtener_id(),
                "nombre": self._nombre,
                "email": self._email,
                "telefono": self._telefono,
                "estado": self.obtener_estado(),
                "fecha_creacion": self.obtener_fecha_creacion().isoformat()
            }
        except Exception as e:
            GestorLogs().registrar_error(e, "Cliente-Serializar")
            return {}


    # ==============================
    # PROPIEDADES (ENCAPSULACIÓN)
    # ==============================

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        try:
            valor = valor.strip()
            if len(valor) < 3:
                raise ErrorValidacion("Nombre inválido")
            self._nombre = valor
        except Exception as e:
            raise ErrorValidacion("Error al actualizar nombre") from e


    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        try:
            valor = valor.strip().lower()
            patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(patron, valor):
                raise ErrorValidacion("Email inválido")
            self._email = valor
        except Exception as e:
            raise ErrorValidacion("Error al actualizar email") from e


    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        try:
            valor = valor.strip()
            if not valor.isdigit() or len(valor) != 10:
                raise ErrorValidacion("Teléfono inválido")
            self._telefono = valor
        except Exception as e:
            raise ErrorValidacion("Error al actualizar teléfono") from e