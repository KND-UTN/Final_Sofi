<template>
  <header class="masthead"
          style="background-image: url('https://media.istockphoto.com/photos/pastel-cyan-blue-green-water-color-paper-texture-background-picture-id1184268799?k=20&m=1184268799&s=170667a&w=0&h=NpfcQndGc7Fa6Vg4OCK0LdxspD8qGYJPqWoEmlPwThE=')">
    <div class="container position-relative px-4 px-lg-5">
      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="py-3 text-center">
          <h1 class="tituloPagina1">Trabajo Pr&aacute;ctico Final</h1>
        </div>
      </div>
    </div>
  </header>
  <div class="container">
    <main>
      <div class="py-4 text-center">
        <p class="lead">
          Proyecto creado en Python y Vue, por Sofía Florencia Cibello [legajo: 79906].
        </p>

        <br>

        <div class="jumbotron jumbotron-fluid">
          <div class="container">
            <h1 class="tituloPagina2">Enunciado</h1>
            <p class="lead">
              A la boleter&iacute;a de una estaci&oacute;n de subtes llegan personas con frecuencia
              variable
              seg&uacute;n el horario:
              <br>
            </p>
            <table class="table table-hover table-sm table-bordered table-striped lead">
              <thead>
              <tr>
                <th>Hora</th>
                <th>Frecuencia</th>
              </tr>
              </thead>
              <tbody>
              <tr>
                <td>7 a 8 hs</td>
                <td>6 +/- 1 seg</td>
              </tr>
              <tr>
                <td>8 a 9 hs</td>
                <td>5 +/- 1 seg</td>
              </tr>
              <tr>
                <td>a partir de las 9 hs</td>
                <td>7 +/- 1 seg</td>
              </tr>
              </tbody>
            </table>
            <p class="lead">En la boletería hay dos empleados que atienden a razón de una persona cada 10
              +/- 4 segundos.
              <br>
              Las personas hacen una cola por cada empleado, eligiendo la ventanilla vacía o,
              en su defecto, la de menor cola. <br>
              Simular 4500 personas atendidas e indicar cual fue la longitud máxima de cola observada.
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>

  <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
    <h1 class="tituloPagina2 text-center">Solución del Ejercicio</h1>

    <h4 class="tituloEnunciado">Datos a ingresar</h4>

    <div class="formulario">
      <div class="container-fluid">
        <fieldset>
          <div class="row">
            <div class="col-sm-4 col-md-3 offset-md-1">
              <label class="col-form-label l">
                Mostrar desde:
              </label>
            </div>
            <div class="col-sm-8 col-md-6">
              <input placeholder="Ingrese un número" required type="number" min="0" v-model="form_simulacion.desde"
                     max="10000000" formcontrolname="MostrarDesde"
                     class="form-control ng-untouched ng-pristine ng-invalid">
            </div>
          </div>
          <br>
          <div class="row">
            <div class="col-sm-4 col-md-3 offset-md-1">
              <label class="col-form-label">
                Mostrar hasta:
              </label>
            </div>
            <div class="col-sm-8 col-md-6">
              <input placeholder="Ingrese un número" required type="number" min="0"
                     max="10000000" formcontrolname="MostrarHasta"
                     class="form-control ng-untouched ng-pristine ng-invalid" v-model="form_simulacion.hasta">
            </div>
          </div>
          <br>
          <div class="row">
            <div class="col-sm-4 col-md-3 offset-md-1">
              <label class="col-form-label">
                Cantidad de atenciones a simular:
              </label>
            </div>
            <div class="col-sm-8 col-md-6">
              <input placeholder="0" required type="number" min="0" max="1000000"
                     formcontrolname="CantAtenciones"
                     class="form-control ng-untouched ng-pristine ng-invalid"
                     v-model="form_simulacion.cant_atenciones_simular">
            </div>
          </div>
          <br>
          <div class="row">
            <div class="col-3 offset-md-1">
              <label class="col-form-label">
                Tiempo de atención desde (segundos):
              </label>
            </div>
            <div class="col-2">
              <input placeholder="0" required type="number" min="0" max="1000000"
                     class="form-control" v-model="form_simulacion.tiempo_atencion.frecuencia_desde">
            </div>
            <div class="col-2">
              <label class="col-form-label">
                Tiempo de atención hasta (segundos):
              </label>
            </div>
            <div class="col-2">
              <input placeholder="0" required type="number" min="0" max="1000000"
                     class="form-control" v-model="form_simulacion.tiempo_atencion.frecuencia_hasta">
            </div>
            <br>
            <div class="row">
              <div class="col-sm-4 col-md-3 offset-md-1">
                <label class="col-form-label">
                  Tiempo de llegada
                </label>
              </div>

            </div>
            <div class="row">
              <div class="col-9 offset-md-1">
                <div class="input-group">
                  <span class="input-group-text">Hora: 7 a 8 hs</span>
                  <input type="number" aria-label="Desde1" placeholder="Desde" class="form-control"
                         min="0" max="10000000" v-model="form_simulacion.tiempo_llegada[0].frecuencia_desde">
                  <input type="number" aria-label="Hasta1" placeholder="Hasta" class="form-control"
                         min="0" max="10000000" v-model="form_simulacion.tiempo_llegada[0].frecuencia_hasta">
                </div>
                <div class="input-group">
                  <span class="input-group-text">Hora: 8 a 9 hs</span>
                  <input type="number" aria-label="Desde2" placeholder="Desde" class="form-control"
                         min="0" max="10000000" v-model="form_simulacion.tiempo_llegada[1].frecuencia_desde">
                  <input type="number" aria-label="Hasta2" placeholder="Hasta" class="form-control"
                         min="0" max="10000000" v-model="form_simulacion.tiempo_llegada[1].frecuencia_hasta">
                </div>
                <div class="input-group">
                  <span class="input-group-text">Hora: 9 a</span>
                  <input type="number" placeholder="hasta" class="form-control" min="0" max="23"
                         v-model="form_simulacion.tiempo_llegada[2].hasta">
                  <span class="input-group-text">hs</span>
                  <input type="number" aria-label="Desde3" placeholder="Desde" class="form-control"
                         min="0" max="10000000" v-model="form_simulacion.tiempo_llegada[2].frecuencia_desde">
                  <input type="number" aria-label="Hasta3" placeholder="Hasta" class="form-control"
                         min="0" max="10000000" v-model="form_simulacion.tiempo_llegada[2].frecuencia_hasta">
                </div>
              </div>
            </div>
            <br>
            <hr class="mt-4">
          </div>
        </fieldset>

      </div>
      <p v-if="!todos_campos_completados" style="color: red"><b>Error:</b> Todos los campos deben ser completados</p>
      <p v-if="!hora_checkeada" style="color: red"><b>Error:</b> La hora de cierre debe ser como máximo la una de la
        mañana</p>
      <div class="row botones justify-content-center">
        <button class="btn btn-primary col-2" @click="getTable"
                style="color: rgb(0, 0, 0); background-color: #c6e9f0; font-weight: bold;">Simular
        </button>
      </div>
    </div>


    <div class="mt-5" v-if="respuesta.length > 0 ">
      <table class="table table-hover table-sm table-bordered table-striped">
        <thead>
        <tr style="text-align: center">
          <th>Simulación</th>
          <th>Evento</th>
          <th>Día</th>
          <th>Reloj</th>
          <th>RND_Llegada</th>
          <th>Tiempo_Llegada (segs)</th>
          <th>Prox_Llegada</th>
          <th>RND_E1</th>
          <th>Tiempo_Atencion_E1 (segs)</th>
          <th>Fin_Atencion_E1</th>
          <th>Estado_E1</th>
          <th>Cola_E1</th>
          <th>RND_E2</th>
          <th>Tiempo_Atencion_E2 (segs)</th>
          <th>Fin_Atencion_E2</th>
          <th>Estado_E2</th>
          <th>Cola_E2</th>
          <th>Cola_Max</th>
          <th>Personas_Atendidas</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="fila in respuesta" v-bind:key="fila.Dia">
          <td>{{ fila.Simulacion }}</td>
          <td>{{ fila.Evento }}</td>
          <td>{{ fila.Dia }}</td>
          <td>{{ fila.Reloj }}</td>
          <td>{{ fila.RND_Llegada }}</td>
          <td>{{ fila.Tiempo_Llegada }}</td>
          <td>{{ fila.Prox_Llegada }}</td>
          <td>{{ fila.RND_E1 }}</td>
          <td>{{ fila.Tiempo_Atencion_E1 }}</td>
          <td>{{ fila.Fin_Atencion_E1 }}</td>
          <td>{{ fila.Estado_E1 }}</td>
          <td>{{ fila.Cola_E1 }}</td>
          <td>{{ fila.RND_E2 }}</td>
          <td>{{ fila.Tiempo_Atencion_E2 }}</td>
          <td>{{ fila.Fin_Atencion_E2 }}</td>
          <td>{{ fila.Estado_E2 }}</td>
          <td>{{ fila.Cola_E2 }}</td>
          <td>{{ fila.Cola_Max }}</td>
          <td>{{ fila.Personas_Atendidas }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'App',
  data() {
    return {
      form_simulacion: {
        'desde': 0,
        'hasta': 100,
        'cant_atenciones_simular': 4500,
        'tiempo_atencion': {
          'frecuencia_desde': 6,
          'frecuencia_hasta': 14
        },
        'tiempo_llegada':
            [
              {'desde': 7, 'hasta': 8, 'frecuencia_desde': 5, 'frecuencia_hasta': 7},
              {'desde': 8, 'hasta': 9, 'frecuencia_desde': 4, 'frecuencia_hasta': 6},
              {'desde': 9, 'hasta': 19, 'frecuencia_desde': 6, 'frecuencia_hasta': 8}
            ]
      },
      respuesta: [],
      todos_campos_completados: true,
      hora_checkeada: true,
    }
  },
  components: {},
  methods: {
    getTable() {
      this.checkearDatos();
      if (this.hora_checkeada && this.todos_campos_completados) {
        const vm = this;
        const form = this.form_simulacion;
        axios.post('http://127.0.0.1:5000/api/procesar', {
          form
        }).then(response => {
          vm.respuesta = response.data
          console.log(vm.respuesta)
        })
      }
    },
    checkearDatos() {
      this.todos_campos_completados = this.form_simulacion.desde !== "" && this.form_simulacion.hasta !== "" &&
          this.form_simulacion.cant_atenciones_simular !== "" && this.form_simulacion.tiempo_atencion.frecuencia_desde !== "" &&
          this.form_simulacion.tiempo_atencion.frecuencia_hasta !== "" &&
          this.form_simulacion.tiempo_llegada[0].frecuencia_desde !== "" &&
          this.form_simulacion.tiempo_llegada[0].frecuencia_hasta !== "" &&
          this.form_simulacion.tiempo_llegada[1].frecuencia_desde !== "" &&
          this.form_simulacion.tiempo_llegada[1].frecuencia_hasta !== "" &&
          this.form_simulacion.tiempo_llegada[2].hasta !== "" &&
          this.form_simulacion.tiempo_llegada[2].frecuencia_desde !== "" &&
          this.form_simulacion.tiempo_llegada[2].frecuencia_hasta !== "";

      this.hora_checkeada = (this.form_simulacion.tiempo_llegada[2].hasta >= 10 &&
              this.form_simulacion.tiempo_llegada[2].hasta <= 23) ||
          this.form_simulacion.tiempo_llegada[2].hasta === 0 ||
          this.form_simulacion.tiempo_llegada[2].hasta === 1;
    }
  },
}
</script>

<style>
.tituloPagina1 {
  font-size: 4.0rem;
  font-weight: 500;
  color: rgb(10, 9, 9);
  border-bottom-style: solid;
  border-bottom-width: thin;
  padding-bottom: 0.1em;
  margin-bottom: 0.5em;
}

.tituloPagina2 {
  font-size: 1.95rem;
  font-weight: 500;
  color: rgb(10, 9, 9);
  border-bottom-style: solid;
  border-bottom-width: thin;
  padding-bottom: 0.1em;
  margin-bottom: 0.5em;
}

.tituloEnunciado {
  font-size: 1.50rem;
  font-weight: 500;
  color: rgb(10, 9, 9);
  padding-bottom: 0.1em;
  margin-bottom: 0.5em;
}

.formulario {
  background-color: rgb(241, 243, 247);
  border-radius: 0.5rem;
  border-style: solid;
  border-color: lightgrey;
  border-width: thin;
  margin: 0em 0.5rem 1rem 0.5rem;
  padding: 0.5rem;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -15px;
  margin-left: -15px;
  color: black;
}

thead {
  color: #000000;
  background-color: #c6e9f0;
  border-color: #dee2e6;
  display: table-header-group;
  vertical-align: middle;
}

tr {
  display: table-row;
  vertical-align: inherit;
  border-color: inherit;
}
</style>
