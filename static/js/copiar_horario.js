// static/js/copiar_horario.js

export function copiarHorario() {
  const entrada = document.querySelector('[name="lunes_entrada"]').value;
  const salida = document.querySelector('[name="lunes_salida"]').value;

  document.querySelectorAll('.copy-checkbox:checked').forEach(cb => {
    const dia = cb.value;
    document.querySelector(`[name="${dia}_entrada"]`).value = entrada;
    document.querySelector(`[name="${dia}_salida"]`).value = salida;
  });
}
