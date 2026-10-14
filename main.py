from views import (
    crear_estudiante, obtener_estudiantes, obtener_estudiante, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, crear_materia, obtener_materias,
    obtener_materia, buscar_materias, actualizar_materia, eliminar_materia,
    materias_sin_cupo, crear_matricula, obtener_matriculas, registrar_nota,
    retirar_matricula, certificado, promedio_de_estudiante
)
from shared.herramientas import limpiar_pantalla, imprimir_color, imprimir_titulo, RESPUESTAS_SI


def pausar():
    input('\nPresiona ENTER para continuar...')


def mostrar_lista(objetos):
    # Polimorfismo: cada modelo tiene su etiqueta()
    if not objetos:
        imprimir_color('No hay registros.', 'amarillo')
        return
    for objeto in objetos:
        imprimir_color(f'ID: {objeto.id} | {objeto.etiqueta()}')


def mostrar_detalle(objeto):
    if objeto is None:
        imprimir_color('Registro no encontrado.', 'rojo')
        return
    imprimir_color(f'ID: {objeto.id} | {objeto.etiqueta()}')
    for campo, valor in objeto.a_diccionario().items():
        if campo != 'id':
            print(f'{campo}: {valor}')


def resultado(respuesta):
    exito, mensaje = respuesta
    imprimir_color(mensaje, 'verde' if exito else 'rojo')


def pedir_campos(campos, objeto=None):
    datos = {}
    for campo in campos:
        valor_anterior = getattr(objeto, campo, '') if objeto else ''
        texto = f'{campo.capitalize()} [{valor_anterior}]: ' if objeto else f'{campo.capitalize()}: '
        valor = input(texto).strip()
        datos[campo] = valor if valor else valor_anterior
    return datos


def menu_entidad(tipo):
    estudiantes = tipo == 'Estudiantes'
    crear = crear_estudiante if estudiantes else crear_materia
    obtener = obtener_estudiantes if estudiantes else obtener_materias
    obtener_uno = obtener_estudiante if estudiantes else obtener_materia
    buscar = buscar_estudiantes if estudiantes else buscar_materias
    actualizar = actualizar_estudiante if estudiantes else actualizar_materia
    borrar = eliminar_estudiante if estudiantes else eliminar_materia
    campos = ('nombre', 'apellido', 'email', 'carnet', 'carrera') if estudiantes else ('nombre', 'codigo', 'creditos', 'cupos')

    while True:
        limpiar_pantalla()
        imprimir_titulo(tipo.upper())
        print('1. Crear\n2. Ver todos\n3. Buscar\n4. Ver por ID\n5. Actualizar\n6. Eliminar\n0. Volver')
        opcion = input('\nSeleccione una opción: ').strip()
        if opcion == '0':
            break
        if opcion == '1':
            resultado(crear(pedir_campos(campos)))
        elif opcion == '2':
            mostrar_lista(obtener())
        elif opcion == '3':
            mostrar_lista(buscar(input('Buscar: ').strip()))
        elif opcion == '4':
            mostrar_detalle(obtener_uno(input('ID: ').strip()))
        elif opcion == '5':
            objeto = obtener_uno(input('ID: ').strip())
            if objeto:
                imprimir_color('Deja vacío para conservar el dato.', 'amarillo')
                resultado(actualizar(objeto.id, pedir_campos(campos, objeto)))
            else:
                imprimir_color('Registro no encontrado.', 'rojo')
        elif opcion == '6':
            objeto = obtener_uno(input('ID: ').strip())
            if objeto:
                mostrar_detalle(objeto)
                if input('¿Desea eliminarlo? (s/n): ').strip().lower() in RESPUESTAS_SI:
                    resultado(borrar(objeto.id))
                else:
                    imprimir_color('Operación cancelada.', 'amarillo')
            else:
                imprimir_color('Registro no encontrado.', 'rojo')
        else:
            imprimir_color('Opción inválida.', 'rojo')
        pausar()


def menu_matriculas():
    while True:
        limpiar_pantalla()
        imprimir_titulo('MATRÍCULAS')
        print('1. Matricular\n2. Ver todas\n3. Registrar nota\n4. Ver certificado\n5. Retirar matrícula\n0. Volver')
        opcion = input('\nSeleccione una opción: ').strip()
        if opcion == '0':
            break
        if opcion == '1':
            datos = {'estudiante_id': input('ID del estudiante: ').strip(),
                     'materia_id': input('ID de la materia: ').strip(),
                     'periodo': input('Periodo (ej. 2026-1): ').strip()}
            resultado(crear_matricula(datos))
        elif opcion == '2':
            mostrar_lista(obtener_matriculas())
        elif opcion == '3':
            resultado(registrar_nota(input('ID de matrícula: ').strip(), input('Nota (0-20): ').strip()))
        elif opcion == '4':
            print(certificado(input('ID de matrícula: ').strip()))
        elif opcion == '5':
            id_registro = input('ID de matrícula: ').strip()
            if input('¿Desea retirarla? (s/n): ').strip().lower() in RESPUESTAS_SI:
                resultado(retirar_matricula(id_registro))
        else:
            imprimir_color('Opción inválida.', 'rojo')
        pausar()


def mostrar_resumen():
    estudiantes = obtener_estudiantes()
    matriculas = obtener_matriculas()
    carreras = {e.carrera for e in estudiantes if e.carrera}  # Set de carreras distintas
    imprimir_titulo('RESUMEN')
    print(f'Estudiantes: {len(estudiantes)}')
    print('Carreras distintas:', ', '.join(sorted(carreras)) or 'Ninguna')
    print('Materias sin cupo:')
    mostrar_lista(materias_sin_cupo())
    print(f'Matrículas aprobadas: {sum(m.esta_aprobada() for m in matriculas)}')
    opcion = input('¿Consultar promedio de un estudiante? (s/n): ').strip().lower()
    if opcion in RESPUESTAS_SI:
        promedio = promedio_de_estudiante(input('ID de estudiante: '))
        print('Sin matrículas' if promedio is None else f'Promedio: {promedio}')


def main():
    while True:
        limpiar_pantalla()
        imprimir_titulo('SISTEMA ACADÉMICO')
        print('1. Estudiantes\n2. Materias\n3. Matrículas\n4. Resumen\n0. Salir')
        opcion = input('\nSeleccione una opción: ').strip()
        if opcion == '1':
            menu_entidad('Estudiantes')
        elif opcion == '2':
            menu_entidad('Materias')
        elif opcion == '3':
            menu_matriculas()
        elif opcion == '4':
            mostrar_resumen()
            pausar()
        elif opcion == '0':
            imprimir_color('Programa finalizado.', 'verde')
            break
        else:
            imprimir_color('Opción inválida.', 'rojo')
            pausar()


if __name__ == '__main__':
    main()
