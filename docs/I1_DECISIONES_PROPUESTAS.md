# I1 — Decisiones para aprobación

Fecha: 2026-10-31, America/Mexico_City. Estado: APROBADO para I1 mediante respuesta explícita del usuario: «Apruebo las recomendaciones para I1». Se conserva el nombre del archivo y el texto de la propuesta para trazabilidad. Este documento continúa la sección «Continuidad y siguiente autorización» de la Fase 0 y no la reemplaza. Quedan autorizadas implementación y pruebas simuladas de I1. I2–I5 están fuera del alcance.

## P04 — Estados y correspondencia

Recomendación: adoptar la tabla siguiente. Toda transición no enumerada se rechaza. Los terminales nunca se reabren; un reintento explícito tiene otro UUID de generación y otro mensaje de respuesta. No reenvío automático.

| Origen | Destinos | Condición |
|---|---|---|
| Creada | Preparando, Cancelada, Fallida | Inicio, cancelación antes del envío, fallo local |
| Preparando | Generando, Cancelando, Fallida | Primer fragmento no vacío, solicitud de cancelación, fallo |
| Generando | Completada, Cancelando, Fallida | Final válido, petición de cancelación, fallo |
| Cancelando | Cancelada, Completada, Fallida | Confirmación del adaptador, terminación normal acreditada antes de surtir efecto la cancelación, fallo |
| Activa de una ejecución anterior | Interrumpida | Solo recuperación explícita; en I1 se simula |
| Completada, Cancelada, Fallida, Interrumpida | Ninguno | Terminal inmutable |

Message del asistente está Pendiente durante los cuatro estados activos; después Completo, Cancelado, Fallido o Interrumpido según Generation. El mensaje del usuario queda Completo cuando se confirma la operación inicial; el fallo posterior de la respuesta no altera su estado. Se conserva el texto parcial con su estado y se excluye del contexto automático. La durabilidad real queda para I2.

Fragmento vacío: no inicia Generando ni añade texto, pero consume su secuencia. Una terminación normal sin texto no blanco es Fallida con error de respuesta vacía (incluso tras fragmentos de espacios). La confirmación de cancelación puede no tener texto. En Cancelando se aceptan fragmentos válidos hasta la evidencia terminal; después ninguno. Un final normal recibido en Cancelando solo completa con evidencia explícita del adaptador de terminación anterior al efecto de cancelación; sin esa evidencia falla como protocolo inconsistente. No se usa la hora del botón como prueba.

Alternativa: clasificar toda solicitud de cancelación como Cancelada. No recomendada: ocultaría respuestas que realmente terminaron y contradice B03577–B03578.

## P05 — Identidades, eventos, orden e idempotencia

Recomendación: UUID independientes para conversación, mensaje, generación, evento y ejecución. Fechas UTC conscientes de zona; secuencia entera creciente por intento para la entrada del proveedor y otra secuencia para los eventos de aplicación. Los IDs se validan junto con sus relaciones, nunca solo por formato.

Cada evento de proveedor lleva conversation_id, generation_id, sequence (desde 1), tipo y payload tipado. Cada evento de aplicación lleva event_id, tipo, fecha y los IDs pertinentes; los de generación incluyen secuencia del coordinador. El adaptador entrega un único flujo ordenado. Un duplicado exacto de secuencia y contenido se ignora; misma secuencia con payload distinto o un salto de secuencia falla el intento por error de protocolo. No hay buffer de reordenamiento. IDs ajenos, intentos viejos y eventos posteriores a terminal se descartan sin contaminar el intento vigente. El adaptador futuro será responsable de normalizar su transporte.

Se conserva el catálogo B03568/T079: conversation.created, conversation.selected, message.submitted, generation.started, generation.chunk_received, generation.completed, generation.cancel_requested, generation.cancelled, generation.failed, message.persisted, provider.disconnected. Se añade generation.interrupted para la recuperación simulada. generation.started significa entrada a Preparando después de la confirmación inicial; el primer texto inicia Generando. message.submitted/message.persisted se emiten tras la confirmación inicial. El evento terminal describe el resultado operativo e indica por separado si se confirmó su guardado. Un guardado final fallido nunca emite message.persisted ni comunica éxito durable.

Una clave de envío (request_id) identifica el intento de envío del cliente: repetirla con los mismos parámetros devuelve el intento existente; reutilizarla con otros parámetros se rechaza. Un reintento voluntario utiliza una nueva clave. La idempotencia de I1 dura la sesión del simulador; la duradera requiere I2.

Alternativa: reordenar eventos con buffer y tiempo de espera. Se difiere: añade memoria, expiraciones y ambigüedad innecesarias para un proveedor con flujo ordenado.

## P07 — Validación y límites de simulación

Recomendación para I1: entrada no vacía y máximo 4.000 caracteres Unicode; salida acumulada máxima 8.000; contexto de entrada máximo 16.000, con reserva separada de 8.000 para salida (presupuesto total 24.000). Se cuentan puntos de código mediante len de Python, no bytes, palabras ni tokens. Rechazar controles NUL y sustitutos Unicode aislados. Se comprueba vacío con strip, pero se conserva el texto original válido. Título entre 1 y 120 caracteres no blancos; límites y descriptores de modelo positivos y coherentes, IDs y roles explícitos.

Construir contexto con instrucciones internas permitidas, pares completos usuario/asistente de intentos completados y el mensaje actual; eliminar los turnos completos más antiguos hasta caber. Nunca cortar una pareja ni resumir. Si instrucciones más mensaje actual no caben, rechazar antes de llamar al proveedor. ModelDescriptor declara roles/capacidades y presupuesto; el contexto y el modelo se congelan por intento. No reenviar automáticamente parciales ni mensajes internos no autorizados para ese proveedor.

Al superar salida, conservar solo el prefijo dentro del límite, solicitar detención y registrar error de recursos; no llamar Completada a una respuesta truncada. Los límites son guardas del simulador, NO equivalencia a capacidad de un modelo real. I3 necesita contabilidad de tokens o una cota validada y límites revisados con su modelo. Alternativa: integrar ahora un tokenizador de modelo; se difiere porque no hay modelo elegido y ampliaría I1.

## P09 y P08/P10 aplicables — Concurrencia y fallos simulados

Recomendación: un coordinador único, propietario de las mutaciones, con exclusión de inicio antes de cualquier espera. Como máximo un intento/proveedor activo en toda la aplicación, incluso entre conversaciones. Segundo envío distinto: rechazo comprensible, sin cola. Cambio de conversación solo cambia selección; cambio de modelo afecta al siguiente intento; cerrar un panel no cancela. Eliminar conversación con intento o recursos de generación activos se rechaza: primero resolverlo y luego confirmar eliminación. No se implementan ventanas.

Proveedor asíncrono cooperativo con recursos de su propiedad; cierre explícito. No crear hilos ilimitados. En I1 la coordinación se prueba en un único event loop mediante barreras y reloj controlable. La integración con trabajadores Qt/SQLite se definirá en I2/I4. Una solicitud de cancelación no libera el cupo. Tras timeout/error, no admitir otro intento hasta confirmar cierre de los recursos del proveedor; si no puede confirmarse, mantener bloqueada la nueva generación y permitir diagnóstico/cierre. Así un terminal lógico no implica que una inferencia anterior haya desaparecido.

Presupuestos del simulador: 30 s hasta primer texto, 30 s de inactividad durante streaming, 120 s totales, 5 s para confirmar cancelación/cierre; cero reintentos automáticos. Un reloj inyectable permite probarlos sin esperar esos tiempos reales. Agotar cancelación sin evidencia produce Fallida, no Cancelada. Estos valores no certifican rendimiento ni configuran Ollama.

Contrato de almacenamiento atómico para mensaje de usuario + solicitud + respuesta pendiente, y para resultado final. I1 usa exclusivamente dobles en memoria con fallos inyectados: fallo inicial impide invocar al proveedor; fallo final conserva resultado operativo y señala guardado no confirmado. No modo temporal alternativo de la aplicación. La memoria de pruebas no es persistencia real y no sobrevive al proceso. Frecuencia de commits parciales, DDL, WAL y recuperación en disco se deciden en I2.

Errores de validación, proveedor, modelo, tiempo, recursos, persistencia, cancelación e internos: código estable, mensaje comprensible e ID de diagnóstico. Sin texto de conversación ni excepciones sin redactar en logs. Las respuestas se tratan como texto sin ejecución de comandos/HTML ni acceso a herramientas.

Alternativas: cola de envíos o cancelar automáticamente al cambiar de vista/modelo. No recomendadas: crean trabajo oculto o interrupciones inesperadas.

## Criterios de prueba previstos (no ejecutados)

| Casos | Evidencia prevista | Requisito/fuente |
|---|---|---|
| Identidad, envío repetido y reintento | Una respuesta por intento; UUID y relaciones válidas | RF-01, B03542–B03554 |
| Transiciones, vacíos y recuperación simulada | Tabla completa; terminal inmutable; Interrumpida | P04, I114/I116, B03636–B03638 |
| Cancelación antes/durante/al terminar | Ambas carreras, confirmación y ausencia de confirmación | RF-04, B03577–B03578, B03618–B03625 |
| Secuencias, duplicados, ajenos y tardíos | Sin pérdida silenciosa ni mezcla | P05, T081 |
| Validación/contexto/salida | Bordes exactos, turnos completos y reserva | RF-02/RF-06 parciales, P07 |
| Dos envíos simultáneos y cambios | Exclusión global y snapshot de modelo/contexto | P09, B03297, B03660 |
| Guardados fallidos y cierres | No invocar antes de commit, no falso guardado, cupo retenido | S-08 simulado, T081 |
| Disponibilidad/modelo/error/timeout | Categorías y diagnóstico sin filtrar contenido | RF-11/RF-12 parciales, T080 |
| Contratos y límites de dependencia | Sin Qt/Ollama/SQL/HTTP en Core; texto inerte | RNF-03/RNF-06/RNF-10 |

No se aceptan mediante I1: inferencia real, UI receptiva, historial durable, recuperación SQLite, modo offline real con modelo, integración Windows, consumo o rendimiento del MVP.

## Procedencia y consecuencias

Base: Prompt maestro A6–A9/A13; Fase 0 «Estados y políticas propuestas», «Decisiones bloqueantes», I1 y continuidad; informe P04/P05/P07/P09. Verificación primaria: Word B03125/T063, B03129/T064, B03241–B03405, B03518–B03735 y atlas T078–T082, I113/I114/I116. Los números, payloads y reglas precisas de este documento son propuestas nuevas; no se atribuyen a capturas ocultas.

La aprobación solicitada cierra únicamente estas decisiones para I1. La autorización de implementar, preparar el entorno y ejecutar pruebas ya está concedida condicionada a ese cierre; no se volverá a pedir. Antes de I2 se presentará esquema/transacciones, selección persistida, política de parciales, recuperación, ruta/retención/borrado/backups/protección (P06/P08/P11) y se solicitará autorización concreta para I2.
