# Registro de preparación de I1

## Actualización posterior al registro inicial

El usuario aprobó expresamente las recomendaciones de I1. La primera escritura se interrumpió por disco lleno: quedaron pyproject.toml y dos __init__.py, sin dominio implementado ni pruebas. Se retiró models.py porque tenía cero bytes y se eliminaron únicamente cachés regenerables de .venv. Las seis fuentes siguieron intactas por SHA-256.

Posteriormente el usuario pausó la implementación hasta «Jarvis go» y pidió commits locales por avance y una bitácora Word didáctica. Informar que ya liberó espacio no reanuda I1. Se comprobó espacio disponible y se inició la preparación de Git y de la bitácora. Los apartados siguientes conservan el registro inicial; las menciones históricas a aprobación pendiente quedan superadas por esta actualización.

Fecha: 2026-10-31, America/Mexico_City.

## Autorización y continuidad

La instrucción actual autoriza inspección, consultas oficiales, entorno aislado, instalación de dependencias gratuitas y documentación sin alterar los originales. Programación y pruebas de I1 están autorizadas una vez aprobadas P04/P05 y políticas aplicables. Se presentó una única solicitud de aprobación de I1_DECISIONES_PROPUESTAS.md. Pendiente de respuesta; el silencio no aprueba. No se programa mientras esté pendiente.

No se rehízo Fase 0. Se retomó su continuidad y su incremento I1. Los antecedentes ausentes no bloquean los requisitos verificados con las fuentes presentes. El diseño conceptual abarca 0.1–2.4; eso no significa versiones de software entregadas.

## Inspección y cobertura real en esta sesión

- Inventario inicial: exactamente los seis archivos indicados, sin código existente. No se encontró AGENTS.md aplicable en la carpeta ni en los ancestros consultados.
- Leídos prompt maestro Markdown (A/B, secciones 1–24), Fase 0 e informe de cobertura con sus decisiones e inventarios. El TXT no se usó como prompt ni se afirma nueva comparación semántica.
- Word: extracción OOXML y lectura directa de texto/tablas pertinentes B03120–B03131, B03241–B03405 y B03518–B03780. Se preservaron filas/celdas en docs/evidence/word-i1-extract.txt. Se verificaron RF/RNF, capas, concurrencia, contratos, estados, eventos, errores y criterios de pruebas.
- Atlas: consultados T078–T082 y extraídas e inspeccionadas visualmente I104, I106, I113, I114, I115, I116. I114 muestra solo Creada → Preparando/Cancelada; I116 un recorrido simplificado y la carrera de cancelación. Ninguna captura acredita una prueba real.
- No se afirma revisión íntegra del Word, de sus 117 imágenes ni de todos los contenidos tempranos; no se renderizó ni certificó paginación. Bxxxxx no son páginas. No se leyeron antecedentes ausentes ni chats previos.
- SHA-256 Word: 887f933f3cc3edbc1ab8c8f6998753018db0d0dffb6cef035db3795dab93d7c0, coincide con el informe. Se registraron las huellas de los seis originales en evidence/source-hashes.json para comprobar conservación.

## Selección técnica y evidencia

Se conserva B03331/T068 y B03385: Python 3.12 x64 y pytest. Se usa el Python base 3.12.14 x64 disponible en el runtime, sin modificarlo. No se presenta como la última versión de Python. El lanzador py no encontró instalaciones registradas; python del PATH apuntaba al alias WindowsApps.

`.venv` se creó mediante venv con include-system-site-packages=false. Sus paquetes no se instalan en el runtime compartido. La documentación oficial explica este aislamiento: https://docs.python.org/3.12/library/venv.html . Licencia de Python: PSF-2.0, https://docs.python.org/3.12/license.html .

Se eligió pytest 9.0.2, versión concreta que admite Python 3.10+ y declara licencia MIT, sin exigir la versión más reciente: https://pypi.org/project/pytest/9.0.2/ . La guía oficial recomienda entorno virtual: https://docs.pytest.org/en/stable/getting-started.html .

Versiones resueltas y fijadas en requirements-dev.txt: pytest 9.0.2, colorama 0.4.6, iniconfig 2.3.1, packaging 26.3, pluggy 1.7.0, Pygments 2.21.0. Metadatos instalados: pytest/iniconfig/pluggy MIT; packaging Apache-2.0 OR BSD-2-Clause; Pygments BSD-2-Clause. Colorama: BSD de tres cláusulas, verificado en su LICENSE.txt instalado (su campo License-Expression no estaba informado). Herramienta pip 25.0.1 incluida por venv, MIT.

No se instalaron PySide6, cliente HTTP, Ollama, tokenizadores, modelos ni bibliotecas de agentes/voz/RAG. I1 no necesita esas dependencias; su selección corresponde a los incrementos que las utilicen. El Core previsto usa biblioteca estándar.

## Comprobaciones ejecutadas, no pruebas de I1

| Comprobación | Resultado real |
|---|---|
| Creación de .venv | Finalizó con código 0 |
| Instalación inicial de pytest dentro del sandbox | Falló por conexión de red bloqueada, WinError 10013 |
| Instalación con mecanismo de permisos del entorno | Completada, seis paquetes instalados |
| python -m pip check | Código 0: No broken requirements found |
| python -m pytest --version | Código 0: pytest 9.0.2 |
| Intérprete aislado | Python 3.12.14, 64 bits, sys.prefix distinto de sys.base_prefix |
| Plataforma reportada por Python | Windows-10-10.0.19045-SP0; no equivale a certificación de compatibilidad del MVP |
| Consulta CIM de equipo/Windows/CPU | Acceso denegado; no se confirmó hardware Dell ni RAM; no necesario para I1 simulado |
| Pruebas de JARVIS | No creadas ni ejecutadas; pendiente aprobación |
| Conservación final de fuentes | Las seis huellas SHA-256 coinciden con el inventario inicial |

No hay resultados de inferencia, tiempos de respuesta de modelo, persistencia, UI ni pruebas de rendimiento reales.

## Archivos añadidos y siguiente paso

README.md orienta la preparación; .gitignore excluye entorno/cachés; requirements-dev.txt fija herramientas. docs/I1_DECISIONES_PROPUESTAS.md contiene opciones, consecuencias, tabla de estados, payloads/reglas y pruebas previstas. Este registro conserva autorización, cobertura y entorno. docs/evidence contiene huellas, extracto de lectura y seis imágenes fuente de consulta; no es evidencia de ejecución del producto.

Tras aprobación: registrar la respuesta, implementar dominio/contratos/coordinación y simuladores, ejecutar pruebas significativas, entregar cobertura trazable y resultados reales. No volver a pedir autorización para esas acciones ya cubiertas.

Antes de I2: revisar resultados de I1 y aprobar P06/P08/P11 (esquema, modelo seleccionado/descriptor, transacciones, parciales, conexiones/WAL, migraciones, recuperación, ruta, retención, borrado, backups y protección), junto con autorización explícita de I2. No es necesario resolver ahora proveedor o interfaz.

Changelog: documentación y preparación de entorno añadidas; implementación ninguna; pruebas de producto ninguna; seguridad del producto sin cambios; sin datos de usuario ni migraciones.
