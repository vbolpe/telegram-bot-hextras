# telegram-bot-hextras

#  Diagrama de Flujo – Bot de Telegram (Dockerizado)

##  Descripción general

Bot de Telegram ejecutándose dentro de un contenedor Docker.  
Gestiona usuarios y registro de horas extras utilizando una base de datos (SQLite).

### Funcionalidades:
- `/start` → Verifica si el usuario existe y lo crea si no
- `/help` → Muestra los comandos disponibles
- `/newh` → Carga una nueva hora extra
- `/csv` → Descarga horas extras de un mes
- Cualquier otro texto → Redirige a `/start`

---

## Flujo general del bot

```mermaid
flowchart TD
    A[Inicio] --> B[Mensaje recibido desde Telegram]
    B --> C{¿Es un comando?}

    C -- NO --> D[Redirigir a /start]
    D --> E

    C -- SI --> E{Comando recibido}

    E -->|/start| F{¿Usuario registrado?}
    F -- NO --> G[Crear usuario en DB]
    G --> H[Confirmar registro]
    F -- SI --> I[Mostrar menú principal]

    E -->|/help| J[Mostrar lista de comandos]

    E -->|/newh| K{¿Usuario registrado?}
    K -- SI --> L[Solicitar datos de hora extra]
    L --> M[Guardar hora extra en DB]
    M --> N[Confirmar carga]

    E -->|/csv| O{¿Usuario registrado?}
    O -- SI --> P[Solicitar mes]
    P --> Q[Buscar horas en DB]
    Q --> R[Generar archivo CSV]
    R --> S[Enviar archivo al usuario]

    E -->|Otro texto| D





 [Inicio]
   |
   v
[Mensaje recibido desde Telegram]
   |
   v
[¿Es un comando?]
   |
   +-- NO --------------------------+
   |                                 |
   v                                 v
[Redirigir a /start]        [Identificar comando]
                                   |
        ------------------------------------------------
        |            |            |           |       |
       /start       /help        /newh        /csv   Otro
        |            |            |           |       |
        v            v            v           v       v
[¿Usuario existe?] [Mostrar      [¿Usuario   [¿Usuario [Redirigir
        |          comandos]     existe?]     existe?] a /start]
   +----+----+                        |           |
   |         |                        |           |
  NO        SI                        SI          SI
   |         |                        |           |
[Crear   [Menú principal]     [Cargar nueva   [Pedir mes]
usuario]                      hora extra]        |
   |                                 |           |
   v                                 v           v
[Confirmar registro]         [Guardar en DB] [Buscar horas]
                                   |           |
                                   v           v
                             [Confirmar OK] [Generar CSV]
                                                   |
                                                   v
                                             [Enviar archivo]



