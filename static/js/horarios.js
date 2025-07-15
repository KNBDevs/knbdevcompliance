// static/js/horarios.js

import { copiarHorario } from './copiar_horario.js';
import { toggleTurnoPartido } from './turno_partido.js';
import { validarHorasTotales, cerrarModal, cerrarModalFaltante } from './validar_horas.js';
import { borrarHorarioDia } from './acciones_horarios.js';
import { iniciarCalendario, obtenerHorariosActuales } from './calendario_horario.js';

document.addEventListener('DOMContentLoaded', () => {

  // Botón copiar horario del lunes
  const copiarBtn = document.getElementById('btn-copiar');
  if (copiarBtn) {
    copiarBtn.addEventListener('click', copiarHorario);
  }

  // Alternar visibilidad del segundo tramo
  document.querySelectorAll('input[type=checkbox][id^="partido_"]').forEach(cb => {
    const dia = cb.id.replace('partido_', '');
    cb.addEventListener('change', () => toggleTurnoPartido(dia));
  });

  // Validación antes de enviar el formulario
  const form = document.getElementById('form-horario');
  if (form) {
    form.addEventListener('submit', function (e) {
      const dias = Array.from(document.querySelectorAll('[name$="_entrada"]'))
        .map(el => el.name.split('_')[0])
        .filter((v, i, a) => a.indexOf(v) === i); // únicos

      if (!validarHorasTotales(dias)) {
        e.preventDefault();
      }
    });
  }

  // Regenerar calendario al cambiar horarios
  document.querySelectorAll('input[type="time"]').forEach(input => {
    input.addEventListener('change', () => {
      iniciarCalendario(obtenerHorariosActuales());
    });
  });

  // Inicializar calendario al cargar
  iniciarCalendario(obtenerHorariosActuales());

  // Exponer funciones a window
  window.cerrarModal = cerrarModal;
  window.cerrarModalFaltante = cerrarModalFaltante;
  window.borrarHorarioDia = borrarHorarioDia;
});
