import random
import datetime

import numpy as np
import pandas as pd

fila = []


class Empleado:
    def __init__(self, frecuencia):
        self.frecuencia_desde = frecuencia['frecuencia_desde']
        self.frecuencia_hasta = frecuencia['frecuencia_hasta']
        self.rnd = self.tiempo_atencion = None
        self.fin_atencion = datetime.datetime(9999, 12, 31, hour=23, minute=59, second=59)
        self.estado = 'Libre'
        self.cola = 0

    def add_persona(self, reloj):
        if self.estado == 'Libre':
            self.calcular_tiempo(reloj)
            self.estado = 'Ocupado'
        elif self.estado == 'Ocupado':
            self.cola += 1
            self.sin_eventos()

    def calcular_tiempo(self, reloj):
        self.rnd = random.random()
        self.tiempo_atencion = self.frecuencia_desde + self.rnd * (self.frecuencia_hasta - self.frecuencia_desde)
        self.fin_atencion = reloj + datetime.timedelta(seconds=self.tiempo_atencion)

    def sin_eventos(self):
        self.rnd = None
        self.tiempo_atencion = None

    def finalizar_atencion(self, reloj, esta_cerrado):
        if esta_cerrado:
            self.cola = 0
            self.estado = 'Libre'
            self.sin_eventos()
            self.fin_atencion = datetime.datetime(9999, 12, 31, hour=23, minute=59, second=59)
        if self.cola > 0:
            self.cola -= 1
            self.calcular_tiempo(reloj)
        else:
            self.estado = 'Libre'
            self.sin_eventos()
            self.fin_atencion = datetime.datetime(9999, 12, 31, hour=23, minute=59, second=59)

    def mostrar(self):
        return [self.rnd, self.tiempo_atencion, self.fin_atencion, self.estado, self.cola]


class GestorEmpleados:
    def __init__(self, frecuencia):
        self.empleado1 = Empleado(frecuencia)
        self.empleado2 = Empleado(frecuencia)

    def add_persona(self, reloj):
        if self.empleado1.estado == 'Libre' or self.empleado1.cola <= self.empleado2.cola:
            self.empleado1.add_persona(reloj)
            self.empleado2.sin_eventos()
        else:
            self.empleado2.add_persona(reloj)
            self.empleado1.sin_eventos()

    def fin_atencion_e1(self, reloj, esta_cerrado):
        self.empleado1.finalizar_atencion(reloj, esta_cerrado)
        self.empleado2.sin_eventos()

    def fin_atencion_e2(self, reloj, esta_cerrado):
        self.empleado2.finalizar_atencion(reloj, esta_cerrado)
        self.empleado1.sin_eventos()

    def mostrar(self):
        return self.empleado1.mostrar() + self.empleado2.mostrar()

    def get_tiempos(self):
        return self.empleado1.fin_atencion, self.empleado2.fin_atencion

    def get_colas(self):
        return self.empleado1.cola, self.empleado2.cola


class Llegada:
    # Esta clase se encarga de calcular el tiempo entre llegadas y las proximas llegadas, teniendo
    # en cuenta las distribuciones establecidas segun el horario.
    def __init__(self, distribuciones):
        # La variable 'distribuciones' debe tener el siguiente formato
        # [
        #     {'desde': 7, 'hasta': 8, 'frecuencia_desde': 5, 'frecuencia_hasta': 7},
        #     {'desde': 8, 'hasta': 9, 'frecuencia_desde': 4, 'frecuencia_hasta': 6},
        #     {'desde': 9, 'hasta': 19, 'frecuencia_desde': 6, 'frecuencia_hasta': 8}
        # ]
        self.distribuciones = distribuciones
        hora_fin_ingresada = distribuciones[2]['hasta']
        self.hora_fin = hora_fin_ingresada if hora_fin_ingresada > 1 else 24 + hora_fin_ingresada

    def calcular_tiempo_llegada(self, reloj):
        reloj: datetime.datetime
        hora = reloj.hour if reloj.hour > 1 else 24 + reloj.hour

        # Devuelve los segundos que faltan para la proxima llegada
        if hora == 7:
            a = self.distribuciones[0]['frecuencia_desde']
            b = self.distribuciones[0]['frecuencia_hasta']
        elif hora == 8:
            a = self.distribuciones[1]['frecuencia_desde']
            b = self.distribuciones[1]['frecuencia_hasta']
        elif 9 <= hora < self.hora_fin:
            a = self.distribuciones[2]['frecuencia_desde']
            b = self.distribuciones[2]['frecuencia_hasta']
        else:
            hora_fin = datetime.datetime(reloj.year, reloj.month, reloj.day,
                                         hour=7) if reloj.hour > 0 else datetime.datetime(reloj.year, reloj.month,
                                                                                          reloj.day + 1, hour=7)
            hasta_prox_apertura = (
                                          hora_fin - reloj).seconds + 1  # Retorna el tiempo (en segundos) que falta hasta la proxima apertura)
            return None, hasta_prox_apertura
        random_num = random.random()
        tiempo_llegada = a + random_num * (b - a)
        nuevo_tiempo_fin = (reloj + datetime.timedelta(seconds=tiempo_llegada)).hour
        nuevo_tiempo_fin = nuevo_tiempo_fin if nuevo_tiempo_fin > 1 else 24 + nuevo_tiempo_fin
        if nuevo_tiempo_fin >= self.hora_fin:
            hora_fin = datetime.datetime(reloj.year, reloj.month, reloj.day,
                                         hour=7) if reloj.hour > 0 else datetime.datetime(reloj.year, reloj.month,
                                                                                          reloj.day + 1, hour=7)
            tiempo_llegada = (
                                          hora_fin - reloj).seconds + 1  # Retorna el tiempo (en segundos) que falta hasta la proxima apertura)
        return random_num, tiempo_llegada

    def esta_cerrado(self, reloj):
        reloj: datetime.datetime
        hora = reloj.hour if reloj.hour > 1 else 24 + reloj.hour
        if hora >= self.hora_fin:
            return True
        return False


class Simulador:
    def __init__(self, datos_entrada):
        # Los datos de entrada deben tener el siguiente formato
        # {
        #     'desde': 0,  # Desde que valor empezar a mostrar
        #     'hasta': 20,  # Hasta que valor mostrar
        #     'cant_atenciones_simular': 4500,  # Cantidad de atenciones a simular
        #     'tiempo_atencion': {
        #         'frecuencia_desde': 6,
        #         'frecuencia_hasta': 14
        #     },
        #     'tiempo_llegada': {
        #         [
        #             {'desde': 7, 'hasta': 8, 'frecuencia_desde': 5, 'frecuencia_hasta': 7},
        #             {'desde': 8, 'hasta': 9, 'frecuencia_desde': 4, 'frecuencia_hasta': 6},
        #             {'desde': 9, 'hasta': 19, 'frecuencia_desde': 6, 'frecuencia_hasta': 8}
        #         ]
        #     }
        # }
        self.datos_entrada = datos_entrada
        self.tabla = []

    def simular(self):
        inf_datetime = datetime.datetime(9999, 12, 31, hour=23, minute=59, second=59)
        gestor_llegadas = Llegada(self.datos_entrada['tiempo_llegada'])
        gestor_empleados = GestorEmpleados(self.datos_entrada['tiempo_atencion'])
        personas_atendidas = num_simulacion = cola_max = 0

        # Inicializacion
        reloj = datetime.datetime(2021, 1, 1, hour=7, minute=0, second=0)
        eventos_nombres = {0: 'Llegada', 1: 'fin_atencion_e1', 2: 'fin_atencion_e2'}
        rnd_llegada, tiempo_llegada = gestor_llegadas.calcular_tiempo_llegada(reloj)
        proximos_eventos = [reloj + datetime.timedelta(seconds=tiempo_llegada), inf_datetime, inf_datetime]
        self.tabla.append([0, 'Inicialización', str(reloj.day), reloj.strftime("%H:%M:%S"), rnd_llegada, tiempo_llegada,
                           proximos_eventos[0].strftime("%H:%M:%S")] + gestor_empleados.mostrar())

        while personas_atendidas < self.datos_entrada['cant_atenciones_simular']:
            num_simulacion += 1
            reloj = min(proximos_eventos)
            evento_actual = proximos_eventos.index(reloj)

            # Llegada nueva
            if evento_actual == 0:
                rnd_llegada, tiempo_llegada = gestor_llegadas.calcular_tiempo_llegada(reloj)
                proximos_eventos[0] = reloj + datetime.timedelta(seconds=tiempo_llegada)
                gestor_empleados.add_persona(reloj)
            else:
                rnd_llegada = tiempo_llegada = None
                personas_atendidas += 1

            if evento_actual == 1:
                gestor_empleados.fin_atencion_e1(reloj, gestor_llegadas.esta_cerrado(reloj))
            elif evento_actual == 2:
                gestor_empleados.fin_atencion_e2(reloj, gestor_llegadas.esta_cerrado(reloj))

            # Cosas que se hacen al final de la simulacion
            proximos_eventos[1], proximos_eventos[2] = gestor_empleados.get_tiempos()
            cola_max = max(cola_max, gestor_empleados.get_colas()[0], gestor_empleados.get_colas()[1])

            if (self.datos_entrada['desde'] <= num_simulacion <= self.datos_entrada['hasta']) or (num_simulacion % 100 == 0) or (personas_atendidas == self.datos_entrada['cant_atenciones_simular']):
                fila_actual = [num_simulacion, eventos_nombres[evento_actual], str(reloj.day),
                               reloj.strftime("%H:%M:%S")]
                # Llegadas
                fila_actual += [rnd_llegada, tiempo_llegada,
                                proximos_eventos[0].strftime("%H:%M:%S")] + gestor_empleados.mostrar()
                fila_actual[9] = None if fila_actual[9] == inf_datetime else fila_actual[9].strftime("%H:%M:%S") if \
                    fila_actual[9] is not None else None
                fila_actual[14] = None if fila_actual[14] == inf_datetime else fila_actual[14].strftime("%H:%M:%S") if \
                    fila_actual[14] is not None else None
                fila_actual += [cola_max, personas_atendidas]

                self.tabla.append(fila_actual)

    def get_table(self):
        # nombres de columna
        column_names = ['Simulacion', 'Evento', 'Dia', 'Reloj', 'RND_Llegada', 'Tiempo_Llegada', 'Prox_Llegada']
        column_names += ['RND_E1', 'Tiempo_Atencion_E1', 'Fin_Atencion_E1', 'Estado_E1', 'Cola_E1']
        column_names += ['RND_E2', 'Tiempo_Atencion_E2', 'Fin_Atencion_E2', 'Estado_E2', 'Cola_E2']
        column_names += ['Cola_Max', 'Personas_Atendidas']
        tabla_mostrar = pd.DataFrame(self.tabla, columns=column_names)
        tabla_mostrar = tabla_mostrar.replace(
            {np.nan: '', datetime.datetime(9999, 12, 31, hour=23, minute=59, second=59): ''})
        return tabla_mostrar.to_json(orient='records', force_ascii=False)


if __name__ == '__main__':
    pd.set_option("display.width", False)
    pd.set_option("display.max_rows", 100000)
    example = {
        'desde': 0,  # Desde que valor empezar a mostrar
        'hasta': 100,  # Hasta que valor mostrar
        'cant_atenciones_simular': 45000,  # Cantidad de atenciones a simular
        'tiempo_atencion': {
            'frecuencia_desde': 6,
            'frecuencia_hasta': 14
        },
        'tiempo_llegada':
            [
                {'desde': 7, 'hasta': 8, 'frecuencia_desde': 5, 'frecuencia_hasta': 7},
                {'desde': 8, 'hasta': 9, 'frecuencia_desde': 4, 'frecuencia_hasta': 6},
                {'desde': 9, 'hasta': 1, 'frecuencia_desde': 6, 'frecuencia_hasta': 10}
            ]
    }
    simulacion = Simulador(example)
    simulacion.simular()
    print(simulacion.get_table())
