# telegram-bot-hextras

# Diagrama de Flujo – Bot de Telegram (Dockerizado)

## Descripcion general

Bot de Telegram ejecutado en Docker que gestiona usuarios y horas extras usando SQLite.

### Comandos soportados
- START → Registro / inicio
- HELP → Lista de comandos
- NEWH → Nueva hora extra
- CSV → Descarga de horas extras
- Texto libre → Redireccion a START

---

## Diagrama de flujo

```mermaid
flowchart TD
    A[Inicio] --> B[Mensaje recibido]
    B --> C{Es comando}

    C -- No --> D[Redirigir a START]
    D --> E[Evaluar comando]

    C -- Si --> E{Tipo de comando}

    E -- START --> F{Usuario existe}
    F -- No --> G[Crear usuario en DB]
    G --> H[Confirmar registro]
    F -- Si --> I[Mostrar menu principal]

    E -- HELP --> J[Mostrar comandos disponibles]

    E -- NEWH --> K{Usuario existe}
    K -- Si --> L[Solicitar datos hora extra]
    L --> M[Guardar hora en DB]
    M --> N[Confirmar carga]

    E -- CSV --> O{Usuario existe}
    O -- Si --> P[Solicitar mes]
    P --> Q[Buscar horas en DB]
    Q --> R[Generar CSV]
    R --> S[Enviar archivo]

    E -- OTRO --> D




