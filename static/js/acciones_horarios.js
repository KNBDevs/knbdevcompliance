// static/js/acciones_horarios.js

export function borrarHorarioDia(dia) {
  const campos = [
    `${dia}_entrada`, `${dia}_salida`,
    `${dia}_entrada_2`, `${dia}_salida_2`
  ];
  campos.forEach(name => {
    const input = document.querySelector(`[name="${name}"]`);
    if (input) input.value = '';
  });

  // Ocultar tramo partido si estaba visible
  const tramo2 = document.getElementById(`tramo2_${dia}`);
  if (tramo2) tramo2.classList.add('hidden');

  const chk = document.getElementById(`partido_${dia}`);
  if (chk) chk.checked = false;
}
