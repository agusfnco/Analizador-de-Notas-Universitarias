## Sistema de Seguimiento Académico

Herramienta de escritorio para registrar materias, notas y analizar
el rendimiento académico. Desarrollado en cuatro versiones progresivas
como proyecto de portfolio.

Tecnologías: Python · Tkinter · matplotlib · reportlab

Funcionalidades:
- Registrar materias y notas con persistencia en JSON
- Interfaz gráfica con formularios y lista dinámica
- Estadísticas descriptivas: promedio, desvío estándar, aprobadas/desaprobadas
- Visualizaciones: promedios por materia, distribución de notas
- Exportación a CSV y PDF

Arquitectura:
  main.py          → punto de entrada y persistencia
  logica.py        → operaciones sobre datos
  gui.py           → interfaz gráfica (Tkinter)
  estadisticas.py  → análisis, gráficos y exportación
