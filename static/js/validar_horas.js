// static/js/validar_horas.js

export function validarHorasTotales(dias) {
  let totalMinutos = 0;

  dias.forEach(dia => {
    totalMinutos += calcularMinutos(dia, '');
    totalMinutos += calcularMinutos(dia, '_2');
  });

  const horasTotales = totalMinutos / 60;
  const maxInput = document.getElementById('max_semanal');
  const max = parseFloat(maxInput.value);

  if (!maxInput.value.trim()) {
    document.getElementById('modalFaltante').classList.remove('hidden');
    return false;
  }

  if (!isNaN(max) && horasTotales > max) {
    const mensaje = horasTotales > 40
      ? `El horario asignado suma ${horasTotales.toFixed(2)}h y supera el máximo de ${max}h. Las horas adicionales serán consideradas horas extras.`
      : `El horario asignado suma ${horasTotales.toFixed(2)}h y supera el máximo de ${max}h.`;

    document.getElementById('mensajeModal').textContent = mensaje;
    document.getElementById('modalHoras').classList.remove('hidden');
    return false;
  }

  return true;
}

function calcularMinutos(dia, sufijo) {
  const entrada = document.querySelector(`[name="${dia}_entrada${sufijo}"]`)?.value;
  const salida = document.querySelector(`[name="${dia}_salida${sufijo}"]`)?.value;

  if (!entrada || !salida) return 0;

  const [h1, m1] = entrada.split(':').map(Number);
  const [h2, m2] = salida.split(':').map(Number);

  return Math.max((h2 * 60 + m2) - (h1 * 60 + m1), 0);
}

export function cerrarModal() {
  document.getElementById('modalHoras').classList.add('hidden');
}

export function cerrarModalFaltante() {
  document.getElementById('modalFaltante').classList.add('hidden');
}
