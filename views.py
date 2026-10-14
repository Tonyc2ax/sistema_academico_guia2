from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON

# Un gestor por entidad
GE = GestorJSON('data/estudiantes.json')
GM = GestorJSON('data/materias.json')
GX = GestorJSON('data/matriculas.json')
CAMPOS_ESTUDIANTE = ('nombre', 'apellido', 'email', 'carnet', 'carrera')  # Tupla fija
CAMPOS_MATERIA = ('nombre', 'codigo')


def leer_objetos(gestor, modelo):
    return [modelo.desde_diccionario(r) for r in gestor.leer()]


def obtener_por_id(gestor, modelo, id_registro):
    try:
        numero = int(id_registro)
    except (ValueError, TypeError):
        return None
    for objeto in leer_objetos(gestor, modelo):
        if objeto.id == numero:
            return objeto
    return None


def buscar(gestor, modelo, texto, campos):
    termino = str(texto).strip().lower()
    if not termino:
        return []
    return [modelo.desde_diccionario(r) for r in gestor.leer()
            if any(termino in str(r.get(c, '')).lower() for c in campos)]


def siguiente_id(gestor):
    ids = [r['id'] for r in gestor.leer()]
    return max(ids) + 1 if ids else 1


def guardar_nuevo(gestor, objeto):
    registros = gestor.leer()
    registros.append(objeto.a_diccionario())
    return gestor.guardar(registros)


def reemplazar(gestor, objeto):
    registros = gestor.leer()
    for i, registro in enumerate(registros):
        if registro['id'] == objeto.id:
            registros[i] = objeto.a_diccionario()
            return gestor.guardar(registros)
    return False


def eliminar(gestor, id_registro):
    registros = gestor.leer()
    nuevos = [r for r in registros if r['id'] != int(id_registro)]
    return len(nuevos) != len(registros) and gestor.guardar(nuevos)


def ids_registrados(gestor):
    return {r['id'] for r in gestor.leer()}  # Set para comprobar IDs


def indice_por_id(objetos):
    return {objeto.id: objeto for objeto in objetos}  # Diccionario para buscar por ID


def es_email_valido(email):
    email = str(email).strip()
    if '@' not in email:
        return False
    usuario, dominio = email.rsplit('@', 1)
    return bool(usuario) and '.' in dominio


def carnets_registrados(excepto_id=None):
    return {r['carnet'].upper() for r in GE.leer() if r['id'] != excepto_id}  # Set evita repetidos


def validar_estudiante(datos, id_actual=None):
    if not all(str(datos.get(c, '')).strip() for c in ('nombre', 'apellido', 'email', 'carnet')):
        return 'Nombre, apellido, email y carnet son obligatorios'
    if not es_email_valido(datos['email']):
        return 'El email no es válido'
    if str(datos['carnet']).upper() in carnets_registrados(id_actual):
        return 'El carnet ya está registrado'
    if str(datos['email']).lower() in {r['email'].lower() for r in GE.leer() if r['id'] != id_actual}:
        return 'El email ya está registrado'
    return None


def crear_estudiante(datos):
    datos = {c: str(datos.get(c, '')).strip() for c in CAMPOS_ESTUDIANTE}
    error = validar_estudiante(datos)
    if error:
        return False, error  # Tupla: resultado y mensaje
    objeto = Estudiante(siguiente_id(GE), **datos)
    return (True, 'Estudiante creado') if guardar_nuevo(GE, objeto) else (False, 'Error al guardar')


def obtener_estudiantes():
    return leer_objetos(GE, Estudiante)


def obtener_estudiante(id_registro):
    return obtener_por_id(GE, Estudiante, id_registro)


def buscar_estudiantes(termino):
    return buscar(GE, Estudiante, termino, CAMPOS_ESTUDIANTE)


def actualizar_estudiante(id_registro, cambios):
    objeto = obtener_estudiante(id_registro)
    if objeto is None:
        return False, 'Estudiante no encontrado'
    datos = objeto.a_diccionario()
    datos.update({k: str(v).strip() for k, v in cambios.items() if k in CAMPOS_ESTUDIANTE})
    error = validar_estudiante(datos, objeto.id)
    if error:
        return False, error
    nuevo = Estudiante(objeto.id, **{c: datos[c] for c in CAMPOS_ESTUDIANTE})
    return (True, 'Estudiante actualizado') if reemplazar(GE, nuevo) else (False, 'Error al guardar')


def eliminar_estudiante(id_registro):
    objeto = obtener_estudiante(id_registro)
    if not objeto:
        return False, 'Estudiante no encontrado'
    if any(m.estudiante_id == objeto.id for m in obtener_matriculas()):
        return False, 'Primero retira sus matrículas'
    return (True, 'Estudiante eliminado') if eliminar(GE, objeto.id) else (False, 'Error al eliminar')


def codigos_registrados(excepto_id=None):
    return {r['codigo'].upper() for r in GM.leer() if r['id'] != excepto_id}  # Set de códigos


def validar_materia(datos, id_actual=None):
    if not str(datos.get('nombre', '')).strip() or not str(datos.get('codigo', '')).strip():
        return 'Nombre y código son obligatorios'
    if str(datos['codigo']).upper() in codigos_registrados(id_actual):
        return 'El código ya existe'
    try:
        creditos, cupos = int(datos['creditos']), int(datos['cupos'])
    except (ValueError, TypeError, KeyError):
        return 'Créditos y cupos deben ser enteros'
    if not 1 <= creditos <= 10:
        return 'Los créditos deben estar entre 1 y 10'
    if not 0 <= cupos <= Materia.CUPOS_MAXIMOS:
        return 'Los cupos deben estar entre 0 y 30'
    return None


def crear_materia(datos):
    error = validar_materia(datos)
    if error:
        return False, error
    objeto = Materia(siguiente_id(GM), str(datos['nombre']).strip(), str(datos['codigo']).strip(),
                     datos['creditos'], datos['cupos'])
    return (True, 'Materia creada') if guardar_nuevo(GM, objeto) else (False, 'Error al guardar')


def obtener_materias():
    return leer_objetos(GM, Materia)


def obtener_materia(id_registro):
    return obtener_por_id(GM, Materia, id_registro)


def buscar_materias(termino):
    return buscar(GM, Materia, termino, CAMPOS_MATERIA)


def actualizar_materia(id_registro, cambios):
    objeto = obtener_materia(id_registro)
    if not objeto:
        return False, 'Materia no encontrada'
    datos = objeto.a_diccionario()
    datos.update({k: v for k, v in cambios.items() if k in ('nombre', 'codigo', 'creditos', 'cupos')})
    error = validar_materia(datos, objeto.id)
    if error:
        return False, error
    ocupados = sum(m.materia_id == objeto.id for m in obtener_matriculas())
    if int(datos['cupos']) + ocupados > Materia.CUPOS_MAXIMOS:
        return False, 'Los cupos superarían el máximo incluyendo matrículas'
    nuevo = Materia(objeto.id, datos['nombre'], datos['codigo'], datos['creditos'], datos['cupos'])
    return (True, 'Materia actualizada') if reemplazar(GM, nuevo) else (False, 'Error al guardar')


def eliminar_materia(id_registro):
    objeto = obtener_materia(id_registro)
    if not objeto:
        return False, 'Materia no encontrada'
    if any(m.materia_id == objeto.id for m in obtener_matriculas()):
        return False, 'Primero retira las matrículas de esta materia'
    return (True, 'Materia eliminada') if eliminar(GM, objeto.id) else (False, 'Error al eliminar')


def materias_sin_cupo():
    return [m for m in obtener_materias() if not m.hay_cupo()]


def crear_matricula(datos):
    try:
        estudiante_id = int(datos['estudiante_id'])
        materia_id = int(datos['materia_id'])
        periodo = str(datos['periodo']).strip()
        nota = float(datos.get('nota', 0))
    except (KeyError, TypeError, ValueError):
        return False, 'Datos de matrícula inválidos'
    if not periodo:
        return False, 'El periodo es obligatorio'
    if estudiante_id not in ids_registrados(GE):
        return False, 'El estudiante no existe'
    materia = obtener_materia(materia_id)
    if not materia:
        return False, 'La materia no existe'
    if not materia.hay_cupo():
        return False, 'No hay cupos disponibles'
    if not Materia.es_nota_valida(nota):
        return False, 'La nota debe estar entre 0 y 20'
    if any(m.estudiante_id == estudiante_id and m.materia_id == materia_id and m.periodo == periodo
           for m in obtener_matriculas()):
        return False, 'Ya existe esta matrícula en el mismo periodo'
    objeto = Matricula(siguiente_id(GX), estudiante_id, materia_id, periodo, nota)
    materia.ocupar_cupo()
    if not reemplazar(GM, materia):
        return False, 'Error al actualizar cupos'
    if not guardar_nuevo(GX, objeto):
        materia.liberar_cupo()
        reemplazar(GM, materia)
        return False, 'Error al guardar matrícula'
    return True, 'Matrícula registrada'


def obtener_matriculas():
    return leer_objetos(GX, Matricula)


def obtener_matricula(id_registro):
    return obtener_por_id(GX, Matricula, id_registro)


def registrar_nota(id_registro, nota):
    matricula = obtener_matricula(id_registro)
    if not matricula:
        return False, 'Matrícula no encontrada'
    if not Materia.es_nota_valida(nota):
        return False, 'La nota debe estar entre 0 y 20'
    matricula.nota = float(nota)
    return (True, 'Nota registrada') if reemplazar(GX, matricula) else (False, 'Error al guardar')


def retirar_matricula(id_registro):
    matricula = obtener_matricula(id_registro)
    if not matricula:
        return False, 'Matrícula no encontrada'
    materia = obtener_materia(matricula.materia_id)
    if not eliminar(GX, matricula.id):
        return False, 'Error al retirar matrícula'
    if materia:
        materia.liberar_cupo()
        if not reemplazar(GM, materia):
            guardar_nuevo(GX, matricula)
            return False, 'Error al devolver el cupo'
    return True, 'Matrícula retirada y cupo devuelto'


def certificado(id_registro):
    matricula = obtener_matricula(id_registro)
    if not matricula:
        return 'Matrícula no encontrada'
    estudiantes = indice_por_id(obtener_estudiantes())  # Índices: diccionarios por ID
    materias = indice_por_id(obtener_materias())
    estudiante = estudiantes.get(matricula.estudiante_id)
    materia = materias.get(matricula.materia_id)
    if not estudiante or not materia:
        return 'Faltan datos del estudiante o materia'
    return (f'CERTIFICADO #{matricula.id}   periodo: {matricula.periodo}\n'
            f'Estudiante: {estudiante.nombre} {estudiante.apellido} ({estudiante.carnet})\n'
            f'Materia   : {materia.nombre} ({materia.codigo}) · {materia.creditos} créditos\n'
            f'------------------------------------------\n'
            f'Nota      : {matricula.nota:g}\nEstado    : {matricula.estado()}')


def matriculas_por_estudiante():
    grupos = {}  # Diccionario de listas, agrupación por estudiante
    for matricula in obtener_matriculas():
        grupos.setdefault(matricula.estudiante_id, []).append(matricula)
    return grupos


def promedio_de_estudiante(id_registro):
    try:
        matriculas = matriculas_por_estudiante().get(int(id_registro), [])
    except (TypeError, ValueError):
        return None
    if not matriculas:
        return None
    return round(sum(m.nota for m in matriculas) / len(matriculas), 2)
