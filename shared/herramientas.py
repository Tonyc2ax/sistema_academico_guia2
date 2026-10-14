import os

COLORES = {'rojo': '\033[91m', 'verde': '\033[92m',
           'amarillo': '\033[93m', 'blanco': '\033[97m',
           'gris': '\033[90m', 'azul': '\033[94m'}
RESPUESTAS_SI = ('si', 'sí', 's', 'yes', 'y')


def limpiar_pantalla():
    if os.environ.get('TERM') or os.name == 'nt':
        os.system('cls' if os.name == 'nt' else 'clear')


def imprimir_color(texto, color='blanco'):
    print(f"{COLORES.get(color, '')}{texto}\033[0m")


def imprimir_titulo(texto):
    imprimir_color('=' * 45, 'azul')
    imprimir_color(texto, 'azul')
    imprimir_color('=' * 45, 'azul')
