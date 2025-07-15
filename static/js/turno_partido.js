// static/js/turno_partido.js

export function toggleTurnoPartido(dia) {
  const seccion = document.getElementById('tramo2_' + dia);
  if (seccion) {
    seccion.classList.toggle('hidden');
  }
}
