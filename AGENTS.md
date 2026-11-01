# Acuerdos de trabajo con el usuario

- Idioma: español claro, explicaciones para quien está aprendiendo Python y SQLite.
- Estado actual: implementación de I1 PAUSADA. Solo reanudar cuando el usuario escriba «Jarvis go» o cambie explícitamente esta regla. Informar que liberó espacio no es reanudación.
- Cuando el usuario interrumpa el flujo, aplicar de nuevo esa espera. La aprobación de las políticas de I1 permanece vigente y no debe solicitarse otra vez.
- Durante esta pausa están solicitados Git local y la bitácora Word del trabajo existente; no continuar lógica de I1 ni sus pruebas.
- Crear commits locales por avances coherentes y revisados. Describir el resultado real, incluidos límites o bloqueos. No crear commits que aparenten implementaciones o pruebas inexistentes.
- Usar la identidad Git ya configurada. No solicitar contraseñas ni publicar o enviar a un remoto sin instrucción del usuario.
- Mantener docs/BITACORA_JARVIS.md como texto editable y generar docs/Bitacora_JARVIS.docx con tools/build_bitacora.py. Explicar propósito, pasos, conceptos, archivos, comprobaciones reales, errores, correcciones y pendientes. La bitácora debe crecer con cada avance relevante.
- Verificar visualmente el Word con la habilidad de documentos. Si falta el renderizador, registrar la limitación y no afirmar revisión visual.
- Conservar intactos los seis originales en la carpeta superior. No añadir .venv, secretos, bases de datos personales o cachés a Git.
- I2–I5, Ollama/modelos, interfaz, voz, RAG, agentes y APIs externas siguen fuera de la autorización actual.
