# Software FJ

Sistema interactivo de consola para gestionar clientes, servicios y reservas. Permite registrar clientes, ofrecer reservas de salas, alquiler de equipos y asesorías especializadas, calcular costos y controlar el estado de las reservas.

## Requisitos

- Python 3.10 o posterior.
- No requiere instalar dependencias externas; utiliza módulos incluidos en Python.

## Ejecución

Desde la carpeta raíz del proyecto, ejecuta:

```bash
python main.py
```

En Windows también puedes usar:

```powershell
py main.py
```

El menú permite registrar un cliente, agregar un servicio, crear y confirmar una reserva, consultar los registros en memoria y finalizar. Al crear una reserva se puede procesar inmediatamente después de confirmarla. Para salir, selecciona **5**.

La carpeta `software_fj/` incluye además `simulation.py`, con una simulación de operaciones válidas y casos de error. Se puede ejecutar con:

```bash
python -m software_fj.simulation
```

## Uso básico

1. Registra un cliente con identificador, nombre, correo y teléfono.
2. Agrega un servicio: reserva de sala, alquiler de equipo o asesoría especializada.
3. Crea una reserva indicando su identificador, el ID del cliente, el ID del servicio y la duración en horas.
4. Confirma la reserva para validar disponibilidad y calcular el costo. Si lo deseas, procésala después.
5. Consulta la información desde el menú. Los datos se mantienen en memoria durante la ejecución.

Los identificadores de clientes y servicios deben ser únicos dentro de su categoría. El programa valida los datos principales, como correo, teléfono, tarifa, capacidad y duración. Una reserva pasa por los estados `PENDIENTE`, `CONFIRMADA`, `CANCELADA` o `PROCESADA`, según las operaciones realizadas.

## Cálculo de costos

El costo base se obtiene multiplicando la tarifa por hora por la duración. Los tipos de servicio aplican estos recargos:

- **Reserva de sala:** tarifa por hora × duración.
- **Alquiler de equipo:** tarifa por hora × duración, más un recargo del 5 %.
- **Asesoría especializada:** tarifa por hora × duración, más un recargo del 15 %.

La clase base de servicio también ofrece métodos para calcular un costo con impuesto (19 % por defecto) o con descuento (10 % por defecto). El flujo de reservas usa el costo normal de cada servicio.

## Estructura del programa

```text
Trabajo UNAD/
├── main.py                         # Punto de entrada del menú interactivo
├── registro_eventos.log            # Archivo de eventos generado durante la ejecución
├── README.md                       # Esta guía
└── software_fj/
    ├── __init__.py
    ├── menu.py                     # Opciones e interacción por consola
    ├── simulation.py               # Escenarios de ejemplo y manejo de errores
    ├── logger.py                   # Registro de eventos en el log
    ├── exceptions.py               # Excepciones propias del sistema
    ├── models/
    │   ├── __init__.py
    │   ├── base.py                 # Entidad abstracta con identificador
    │   ├── client.py                # Modelo Cliente y validaciones
    │   ├── services.py              # Servicio y sus tres tipos concretos
    │   └── reservation.py           # Reserva y transiciones de estado
    └── services/
        ├── __init__.py
        └── system.py               # Administración de clientes, servicios y reservas
```

### Responsabilidades principales

- **`main.py`:** inicia el menú y captura errores críticos no controlados.
- **`software_fj/menu.py`:** solicita los datos al usuario y llama a las operaciones del sistema.
- **`software_fj/services/system.py`:** mantiene las listas de clientes, servicios y reservas durante la sesión; valida relaciones e identificadores.
- **`software_fj/models/`:** define las entidades, sus validaciones, descripciones y reglas de cálculo.
- **`software_fj/exceptions.py`:** agrupa errores de validación, disponibilidad y reservas.
- **`software_fj/logger.py`:** agrega eventos y errores a `registro_eventos.log` en la carpeta desde la que se ejecuta el programa.
- **`software_fj/simulation.py`:** ejecuta una demostración programada, independiente del menú principal.

## Persistencia y logs

Los clientes, servicios y reservas solo se guardan en memoria, por lo que se pierden al cerrar el programa. Los eventos se agregan al archivo `registro_eventos.log`; el archivo se crea si no existe. Su ubicación depende del directorio de trabajo desde el que se ejecute Python.

## Manejo de errores

Los errores esperados del sistema se muestran en consola y se registran cuando corresponde. Si un dato numérico no se puede convertir, el menú informa que debe revisarse. Si ocurre una excepción crítica fuera del flujo esperado, `main.py` registra el error e indica que se revise el log.
