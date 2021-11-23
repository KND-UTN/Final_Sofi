import json

from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS

from simulacion import Simulador

app = Flask(__name__, template_folder='webpage\\dist',
                static_url_path='',
                static_folder='webpage\\dist')
CORS(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/procesar', methods=['POST'])
def procesar():
    print(request.json)
    resultado = request.json['form']
    datos = {
        'desde': int(resultado['desde']),  # Desde que valor empezar a mostrar
        'hasta': int(resultado['hasta']),  # Hasta que valor mostrar
        'cant_atenciones_simular': int(resultado['cant_atenciones_simular']),  # Cantidad de atenciones a simular
        'tiempo_atencion': {
            'frecuencia_desde': int(resultado['tiempo_atencion']['frecuencia_desde']),
            'frecuencia_hasta': int(resultado['tiempo_atencion']['frecuencia_hasta'])
        },
        'tiempo_llegada':
            [
                {'desde': 7, 'hasta': 8, 'frecuencia_desde': int(resultado['tiempo_llegada'][0]['frecuencia_desde']),
                 'frecuencia_hasta': int(resultado['tiempo_llegada'][0]['frecuencia_hasta'])},
                {'desde': 8, 'hasta': 9, 'frecuencia_desde': int(resultado['tiempo_llegada'][1]['frecuencia_desde']),
                 'frecuencia_hasta': int(resultado['tiempo_llegada'][1]['frecuencia_hasta'])},
                {'desde': 9, 'hasta': int(resultado['tiempo_llegada'][2]['hasta']),
                 'frecuencia_desde': int(resultado['tiempo_llegada'][2]['frecuencia_desde']),
                 'frecuencia_hasta': int(resultado['tiempo_llegada'][2]['frecuencia_hasta'])}
            ]
    }

    simulador = Simulador(datos)
    simulador.simular()
    return jsonify(json.loads(simulador.get_table()))


if __name__ == '__main__':
    app.run()
