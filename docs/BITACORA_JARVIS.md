# Bitácora de desarrollo de JARVIS

## Edición inicial y estado del proyecto

Esta bitácora explica el trabajo realizado para preparar JARVIS y enseña los conceptos que aparecen durante su construcción. Está dirigida a su propietario, que está aprendiendo Python y SQLite. Codex registra las acciones; el usuario decide el alcance y las autorizaciones.

**Situación actual.** La preparación del entorno está hecha y las políticas de I1 están aprobadas. La implementación sigue pausada hasta que el usuario escriba «Jarvis go». Ya existe un repositorio Git local. No existe todavía un asistente capaz de conversar con un modelo real.

I1 significa «dominio y contratos con proveedor simulado». Su objetivo será comprobar reglas: qué identifica una conversación, cómo se cancela una respuesta y qué ocurre si llegan datos repetidos o fallan los guardados. Un simulador produce datos controlados para probar esas situaciones. No piensa ni consulta un modelo.

### Cómo leer esta bitácora

Cada entrada explica qué se buscaba, qué se hizo y qué resultado se obtuvo. Los ejemplos ayudan a entender; solo se consideran ejecutados los comandos cuyo resultado se registra expresamente. Una decisión aprobada tampoco significa que ya esté programada.

El registro inicial de preparación tiene fecha 31 de octubre de 2026. Los acontecimientos posteriores se presentan en orden de la conversación, sin inventar horas o fechas. Git conserva por separado la fecha de cada commit según el reloj del equipo.

### Regla de continuidad

Cuando el usuario interrumpe el flujo, la implementación espera «Jarvis go». Avisar que se liberó espacio permite atender el bloqueo y preparar la documentación solicitada, pero no reanuda I1. Esta regla y el compromiso de mantener commits y bitácora están escritos en AGENTS.md.

<!-- page -->

## Paso 1 Comprender las fuentes

**Objetivo.** Empezar desde la documentación disponible sin rehacer la Fase 0 ni confundir ideas futuras con funciones actuales.

Primero se inspeccionó la carpeta C:\Users\Hello\Desktop\JARVIS. Contenía seis documentos y ningún proyecto de código. Se leyeron el prompt maestro Markdown, la Fase 0 y el informe de cobertura. El TXT se conservó como versión alternativa; no se utilizó en lugar del Markdown.

Después se contrastaron los requisitos pertinentes con texto y tablas del Word y con el atlas. La revisión primaria abarcó los bloques B03120–B03131, B03241–B03405 y B03518–B03780; se inspeccionaron las imágenes I104, I106, I113, I114, I115 e I116. Los identificadores B son localizadores editoriales, no páginas.

**Resultado.** La documentación contiene diseño conceptual 0.1–2.4. Los antecedentes antiguos ausentes no impiden comenzar I1 porque sus requisitos necesarios tienen respaldo en las fuentes disponibles. No se afirmó haber revisado íntegramente el Word ni todas sus imágenes.

### Qué es una huella de archivo

Se calcularon huellas SHA-256 de los seis originales. Una huella es una cadena calculada a partir de los bytes del archivo. Si el contenido cambia, normalmente cambia también la huella. Compararla antes y después permite comprobar que no alteramos las fuentes.

Las comprobaciones realizadas confirmaron que los seis originales permanecían intactos. Sus huellas se guardaron en docs/evidence/source-hashes.json. Las imágenes y el extracto de esa carpeta son copias de consulta; no son resultados de pruebas del software.

### Lo que aprendemos

Documentar una idea, aprobar una regla, escribir código y probarlo son pasos distintos. Mantener esa diferencia evita decir «JARVIS funciona» cuando solo tenemos una especificación o un dibujo.

<!-- page -->

## Paso 2 Preparar un entorno separado

**Objetivo.** Crear un lugar de trabajo que no modifique los documentos fuente ni mezcle dependencias del proyecto con otras herramientas del equipo.

Se creó jarvis-app dentro de la carpeta original. Allí se preparó .venv usando el Python 3.12.14 de 64 bits disponible en el entorno. Un entorno virtual es una carpeta con su propio acceso a Python y sus paquetes. Permite que este proyecto use versiones concretas sin instalarlas globalmente.

Se instaló pytest 9.0.2 y sus dependencias en .venv. Pytest es una herramienta para ejecutar comprobaciones automáticas: una prueba prepara una situación, realiza una operación y compara el resultado con lo esperado. Instalar pytest no crea las pruebas por sí solo.

### Comprobaciones que sí se ejecutaron

El comando siguiente terminó correctamente e informó «No broken requirements found». Significa que los paquetes instalados satisfacen sus dependencias declaradas.

```powershell
.\.venv\Scripts\python.exe -m pip check
```

Este otro comando mostró «pytest 9.0.2». Comprueba que la herramienta puede arrancar; no prueba las funciones de JARVIS.

```powershell
.\.venv\Scripts\python.exe -m pytest --version
```

Estos comandos se ejecutan desde jarvis-app. La ruta explícita al Python de .venv evita depender de qué Python tenga prioridad en el sistema.

### Dificultad y solución

La primera instalación falló porque el entorno bloqueó la conexión de red. Se utilizó su mecanismo de permisos y la instalación terminó. Las versiones quedaron fijadas en requirements-dev.txt. No se instalaron Ollama, modelos, PySide6 ni servicios externos.

La consulta de hardware mediante CIM devolvió acceso denegado. Por eso no se confirmó que el equipo actual fuera el Dell histórico. Ese dato no impide preparar I1 con simulaciones.

<!-- page -->

## Paso 3 Aprobar las reglas antes del código

**Objetivo.** Resolver comportamientos que no conviene improvisar durante la programación. Las recomendaciones completas están en docs/I1_DECISIONES_PROPUESTAS.md y fueron aprobadas con la respuesta «Apruebo las recomendaciones para I1».

### Estados y cancelación

Una generación representa un intento de respuesta. Puede estar Creada, Preparando, Generando o Cancelando, y terminar Completada, Cancelada, Fallida o Interrumpida. Un estado terminal no vuelve a estar activo. Un reintento necesita una identidad nueva.

Pedir cancelar no prueba que el proveedor ya se detuvo. Si terminó realmente antes de que la cancelación surtiera efecto, el resultado puede ser Completada. Si no hay evidencia suficiente, no se inventa una confirmación. La recuperación de Interrumpida se simulará en I1; la recuperación en disco corresponde a I2.

### Identidades y mensajes repetidos

Cada conversación, mensaje e intento tendrá identificadores. Los fragmentos llevarán una secuencia para comprobar el orden. Un duplicado exacto se ignorará; una secuencia contradictoria producirá un error. Un fragmento de una generación antigua no podrá entrar en la nueva.

Ejemplo didáctico: si llegan «Ho» y «la», la respuesta es «Hola». Si «Ho» llega dos veces con la misma identidad de fragmento, no debe convertirse en «HoHola». Esta prueba todavía no se ha implementado.

### Límites y concurrencia

Los límites aprobados para la simulación son 4.000 caracteres de entrada, 16.000 de contexto y 8.000 de salida. Se recortarán turnos antiguos completos. Caracteres y tokens no son la misma unidad: los límites de un modelo real se definirán después.

Habrá una generación activa global como máximo, sin cola oculta. Cambiar de conversación solo cambiará la selección; cambiar de modelo afectará al siguiente turno. Se comprobarán fallos de guardado con dobles en memoria, sin presentar esa memoria como SQLite real.

<!-- page -->

## Paso 4 Registrar la interrupción y el estado real

**Lo ocurrido.** Después de la aprobación se intentó escribir el primer conjunto de archivos. El disco llegó a cero bytes disponibles y Windows rechazó la escritura. También dejó de poder iniciar algunos comandos.

Se comprobó qué se había creado: pyproject.toml y dos archivos __init__.py. El archivo models.py había quedado vacío y se retiró. Se eliminaron únicamente cachés regenerables de .venv. Eso no solucionó entonces la falta de espacio. No se ejecutaron pruebas de JARVIS.

El usuario pidió pausar el flujo hasta «Jarvis go» y añadir Git y una bitácora Word. Más tarde informó que había liberado espacio. La comprobación posterior mostró aproximadamente 36 GB libres. El bloqueo de almacenamiento quedó resuelto, pero la pausa de implementación continúa.

### Para qué sirve cada archivo actual

**README.md** es la entrada al proyecto: explica su estado y cómo usar el entorno preparado.

**requirements-dev.txt** enumera las versiones de las herramientas de desarrollo. **.venv** contiene el entorno instalado y se excluye de Git.

**pyproject.toml** declara el nombre del proyecto, su versión de trabajo, la versión de Python prevista y la configuración de pytest. Su presencia no implica que el dominio esté implementado.

**src/jarvis/__init__.py** y **src/jarvis/domain/__init__.py** son los dos archivos iniciales que alcanzaron a escribirse. No contienen lógica de conversación, cancelación ni proveedores.

**docs/I1_PREPARACION.md** conserva la revisión, las herramientas y sus comprobaciones. **docs/I1_DECISIONES_PROPUESTAS.md** conserva las políticas aprobadas; su nombre histórico no significa que sigan pendientes.

**AGENTS.md** registra las reglas de trabajo. **.gitignore** evita guardar entornos y cachés en Git. **.gitattributes** ayuda a tratar correctamente archivos de texto y documentos binarios.

**Resultado actual.** Hay preparación y una estructura inicial incompleta. No hay contratos ejecutables, proveedor simulado, base de datos ni pruebas del producto. La siguiente implementación solo comienza tras la palabra acordada.

<!-- page -->

## Paso 5 Guardar avances con Git

Git conserva instantáneas de archivos seleccionados. Cada instantánea se llama commit y tiene un identificador, un autor y un mensaje. Sirve para revisar cambios y volver a consultar estados anteriores. Un commit local no publica nada en Internet.

Se comprobó que jarvis-app no pertenecía a un repositorio y se inicializó uno en esa misma carpeta, en la rama codex/i1-preparacion. Se utilizó la identidad de Git que ya estaba configurada. No se solicitaron contraseñas ni se configuró un remoto.

### Primer punto de control

Se revisaron los archivos seleccionados y se creó el commit **6b5a1ed**, con el mensaje «chore: registrar preparacion de I1 y pausa autorizada». Contiene la preparación existente, las decisiones aprobadas, la evidencia de consulta y el estado pausado. No se etiquetó como implementación terminada.

Git detectó espacios al final de algunas líneas del extracto del Word. Se preservó el extracto y se configuró una excepción de revisión de espacios solo para ese archivo de consulta. La comprobación de formato del contenido preparado terminó después sin errores.

### Cómo entender el ciclo de un commit

Primero se revisa qué cambió. Después se seleccionan los archivos que forman un avance coherente. Se comprueba el contenido seleccionado y, finalmente, se crea el commit con un mensaje fiel al resultado. No se harán commits por cada tecla ni se dirá que una prueba pasó si no fue ejecutada.

Para consultar el historial desde jarvis-app se puede usar:

```powershell
git log --oneline
git status --short
```

El primero muestra los commits; el segundo muestra cambios todavía pendientes. Estos comandos consultan el repositorio, no ejecutan JARVIS. Si git no se reconoce en una terminal nueva, puede usarse la ruta del ejecutable disponible en el equipo.

La bitácora y las reglas de continuidad se guardarán en un commit separado. Su identificador se consulta en Git para evitar que el documento tenga que incluir el hash del mismo commit que lo contiene.

<!-- page -->

## Paso 6 Mantener la bitácora y continuar

El texto editable vive en docs/BITACORA_JARVIS.md. La copia Word se genera como docs/Bitacora_JARVIS.docx mediante tools/build_bitacora.py. El generador es una herramienta de documentación; no forma parte del dominio ni reanuda I1.

La bitácora se actualizará cuando exista un avance coherente. Se añadirá qué problema se atendió, qué archivos cambiaron, cómo se comprobó el resultado y qué falta. Las entradas anteriores conservarán su contexto; una corrección se señalará como tal. Los errores también se documentan porque ayudan a aprender y a reproducir el trabajo.

### Comprobaciones de esta edición

Se verificaron el espacio disponible, el estado inicial de Git, la identidad configurada y los archivos que quedaron tras el fallo. Se creó el primer commit y se registró la pausa. La validación visual del Word se registra aparte en docs/REVISION_BITACORA.md: crear el archivo y comprobar su texto no demuestran que su paginación sea correcta.

No se han ejecutado pruebas de dominio, contratos, cancelación ni concurrencia. No se han medido rendimiento de inferencia, interfaz o recuperación SQLite. Las comprobaciones anteriores de pip y de la versión de pytest solo validaron la preparación de herramientas.

### Próximo avance de implementación

Después de «Jarvis go» se retomará I1: entidades y contratos independientes de Qt y Ollama, coordinación de una sola generación y simuladores con pruebas significativas. Se registrarán los resultados reales y se crearán commits por avances revisados. No será necesario volver a aprobar las políticas ya aceptadas.

Antes de I2 se propondrán el esquema SQLite, las transacciones, el guardado de parciales, la recuperación, la ubicación de datos y las políticas de retención, borrado y respaldo. I2 necesita su autorización propia.

### Fuentes para volver a consultar

La Fase 0 y el prompt maestro se encuentran en la carpeta superior. El detalle de lo inspeccionado está en I1_PREPARACION.md y las reglas en I1_DECISIONES_PROPUESTAS.md. La documentación oficial consultada durante la preparación fue docs.python.org/3.12/library/venv.html, docs.python.org/3.12/license.html, docs.pytest.org/en/stable/getting-started.html y pypi.org/project/pytest/9.0.2/.

**Idea clave.** Un avance confiable tiene una explicación, archivos identificables y evidencia proporcional. Todavía estamos construyendo las bases de JARVIS.
