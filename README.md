# Sistema Académico — Guía 2

Sistema de estudiantes, materias y matrículas en Python, con MVC, herencia y polimorfismo.

## Ejecutar

Desde la carpeta del proyecto:

```bash
python main.py
```

## Archivos

- `models.py`: clases `ModeloBase`, `Persona`, `Estudiante`, `Materia` y `Matricula`.
- `views.py`: validaciones, CRUD y operaciones de matrícula.
- `main.py`: menús de consola.
- `shared/`: utilidades de consola y persistencia JSON.
- `data/`: estudiantes, materias y matrículas guardados por separado.

## Funciones

CRUD de estudiantes y materias, carnet/código/email únicos, créditos y cupos válidos, matrícula sin duplicados, notas entre 0 y 20, certificados, resumen y promedios.
