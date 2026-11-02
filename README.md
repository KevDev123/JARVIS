# J.A.R.V.I.S. — Preparación de I1

Estado: políticas de I1 aprobadas; implementación pausada por instrucción del usuario hasta «Jarvis go». La falta de espacio interrumpió la primera escritura. Solo existen pyproject.toml y dos archivos __init__.py iniciales; todavía no hay lógica de I1 ni pruebas. Este directorio continúa la Fase 0 existente; los seis documentos fuente permanecen en la carpeta superior sin modificaciones.

Leer [decisiones aprobadas](docs/I1_DECISIONES_PROPUESTAS.md) y [registro de preparación](docs/I1_PREPARACION.md). La aprobación de I1 permanece vigente, pero la pausa posterior impide continuar su implementación hasta la palabra de reanudación. Preparar Git y la bitácora sí está solicitado. No están autorizados I2–I5.

## Entorno preparado

Python 3.12.14 x64, pytest 9.0.2, dependencias aisladas en `.venv`. No hace falta activar el entorno ni cambiar la política de ejecución de PowerShell:

```powershell
Set-Location 'C:\Users\Hello\Desktop\JARVIS\jarvis-app'
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest --version
```

Estos comandos verifican herramientas; no prueban JARVIS. Cuando existan las pruebas de I1, se documentará y ejecutará `.\.venv\Scripts\python.exe -m pytest`. Ejecutarlo ahora no acredita nada: no hay pruebas creadas.

Para recrear este entorno en esta computadora usando el intérprete disponible:

```powershell
& 'C:\Users\Hello\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

En otra computadora se requiere un Python 3.12 x64 disponible y se sustituye la ruta del intérprete. El entorno depende de su Python base y no debe copiarse entre computadoras. Las versiones fijadas registran lo instalado; no se han archivado ruedas para instalación sin red.

I1 se limitará a dominio, contratos, coordinación y dobles de prueba en memoria. No conversa con modelos reales ni guarda historial durable. SQLite y recuperación real corresponden a I2; Ollama a I3; interfaz a I4; aceptación global a I5.

## Seguimiento del trabajo

La rama `main` sigue a `origin/main` en [KevDev123/JARVIS](https://github.com/KevDev123/JARVIS). El primer commit `6b5a1ed` conserva la preparación. El siguiente, `b64fff4`, añade la bitácora y los acuerdos de continuidad.

La [bitácora didáctica](docs/BITACORA_JARVIS.md) explica los pasos y conceptos. Su copia Word está creada en `docs/Bitacora_JARVIS.docx`, como borrador pendiente de revisión visual: falta el renderizador LibreOffice del entorno. Consulta [el registro de revisión](docs/REVISION_BITACORA.md). `tools/build_bitacora.py` la genera con el runtime documental; no es código de I1 y no añade dependencias al Core.

Las instrucciones persistentes están en [AGENTS.md](AGENTS.md). La implementación continúa esperando «Jarvis go».
