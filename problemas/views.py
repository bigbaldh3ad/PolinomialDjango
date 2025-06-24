from django.shortcuts import render
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

PROBLEMAS_REALES = {
    'caida_libre': {
        'titulo': 'Caída libre (altura vs tiempo)',
        'descripcion': 'Altura de un objeto que cae en el vacío (sin resistencia del aire).',
        'datos_x': '0,1,2,3,4',
        'datos_y': '0,4.9,19.6,44.1,78.4',
        'grado': 2
    },
    'crecimiento_bacteriano': {
        'titulo': 'Crecimiento bacteriano (población vs tiempo)',
        'descripcion': 'Número de bacterias en una colonia en crecimiento.',
        'datos_x': '0,1,2,3,4',
        'datos_y': '100,180,325,600,1100',
        'grado': 3
    },
    'enfriamiento_newton': {
        'titulo': 'Enfriamiento según Newton',
        'descripcion': 'Temperatura de un objeto caliente en función del tiempo.',
        'datos_x': '0,1,2,3,4',
        'datos_y': '100,80,65,54,46',
        'grado': 2
    },
}

def index(request):
    resultado = None
    error = None
    datos_x = datos_y = grado = ''
    seleccionado = ''
    imagen_grafica = None

    if request.method == 'POST':
        try:
            if 'problema' in request.POST and request.POST['problema']:
                seleccionado = request.POST['problema']
                problema = PROBLEMAS_REALES.get(seleccionado)
                datos_x = problema['datos_x']
                datos_y = problema['datos_y']
                grado = problema['grado']
            else:
                datos_x = request.POST['datos_x']
                datos_y = request.POST['datos_y']
                grado = int(request.POST['grado'])

            lista_x = list(map(float, datos_x.split(',')))
            lista_y = list(map(float, datos_y.split(',')))

            if len(lista_x) != len(lista_y):
                raise ValueError("X y Y deben tener la misma cantidad de datos")

            coef = np.polyfit(lista_x, lista_y, int(grado))
            polinomio = np.poly1d(coef)
            resultado = str(polinomio)

            # Crear puntos para la curva
            curva_x = np.linspace(min(lista_x), max(lista_x), 100)
            curva_y = polinomio(curva_x)

            plt.figure(figsize=(7, 4))
            plt.plot(curva_x, curva_y, label='Curva ajustada', color='blue')
            plt.scatter(lista_x, lista_y, label='Datos originales', color='red')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Ajuste polinomial')
            plt.legend()
            plt.grid(True)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            imagen_grafica = base64.b64encode(buf.read()).decode('utf-8')

        except Exception as e:
            error = str(e)

    problema_seleccionado = PROBLEMAS_REALES.get(seleccionado) if seleccionado else None

    return render(request, 'problemas/index.html', {
        'resultado': resultado,
        'error': error,
        'problemas': PROBLEMAS_REALES,
        'datos_x': datos_x,
        'datos_y': datos_y,
        'grado': grado,
        'seleccionado': seleccionado,
        'problema_seleccionado': problema_seleccionado,
        'imagen_grafica': imagen_grafica
    })

from django.shortcuts import render

def home(request):
    return render(request, 'problemas/home.html')
