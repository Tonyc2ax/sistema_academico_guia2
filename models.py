from datetime import date


class ModeloBase:
    def __init__(self, id_registro):
        self.id = int(id_registro)

    @classmethod
    def desde_diccionario(cls, datos):
        datos = dict(datos)
        id_registro = datos.pop('id')
        return cls(id_registro, **datos)

    def a_diccionario(self):
        return {'id': self.id}

    def etiqueta(self):
        return f'Registro {self.id}'

    def __str__(self):
        return self.etiqueta()


class Persona(ModeloBase):
    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({'nombre': self.nombre, 'apellido': self.apellido, 'email': self.email})
        return datos

    def etiqueta(self):
        return f'{self.nombre} {self.apellido}'


class Estudiante(Persona):
    def __init__(self, id_registro, nombre, apellido, email, carnet='', carrera=''):
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({'carnet': self.carnet, 'carrera': self.carrera})
        return datos

    def etiqueta(self):
        return f'{super().etiqueta()} · {self.carnet} · {self.carrera}'


class Materia(ModeloBase):
    CUPOS_MAXIMOS = 30
    NOTA_APROBACION = 14

    def __init__(self, id_registro, nombre, codigo, creditos=0, cupos=0):
        super().__init__(id_registro)
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = int(creditos)
        self.cupos = int(cupos)

    @staticmethod
    def es_nota_valida(valor):
        try:
            return 0 <= float(valor) <= 20
        except (TypeError, ValueError):
            return False

    def hay_cupo(self):
        return self.cupos > 0

    def ocupar_cupo(self):
        if self.hay_cupo():
            self.cupos -= 1
            return True
        return False

    def liberar_cupo(self):
        if self.cupos < Materia.CUPOS_MAXIMOS:
            self.cupos += 1
            return True
        return False

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({'nombre': self.nombre, 'codigo': self.codigo,
                      'creditos': self.creditos, 'cupos': self.cupos})
        return datos

    def etiqueta(self):
        return f'{self.nombre} · {self.codigo} · {self.creditos} créditos · {self.cupos} cupos'


class Matricula(ModeloBase):
    def __init__(self, id_registro, estudiante_id, materia_id, periodo, nota=0, fecha=''):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = periodo
        self.nota = float(nota)
        self.fecha = fecha or date.today().isoformat()

    def esta_aprobada(self):
        return self.nota >= Materia.NOTA_APROBACION

    def estado(self):
        return 'Aprobado' if self.esta_aprobada() else 'Reprobado'

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({'estudiante_id': self.estudiante_id,
                      'materia_id': self.materia_id, 'periodo': self.periodo,
                      'nota': self.nota, 'fecha': self.fecha})
        return datos

    def etiqueta(self):
        return (f'{self.periodo} · estudiante {self.estudiante_id} · '
                f'materia {self.materia_id} · nota {self.nota:g} · {self.estado()}')
