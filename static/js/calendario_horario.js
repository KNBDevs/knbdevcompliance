// static/js/calendario_horario.js

export function iniciarCalendario(horarios) {
  const calendario = document.getElementById('calendarioHorario');
  const popup = document.getElementById('popupTramos');
  const hoy = new Date();
  const year = hoy.getFullYear();
  const month = hoy.getMonth();
  const diasMes = new Date(year, month + 1, 0).getDate();

  const diasSemana = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];

  // Encabezado con días de la semana
  calendario.innerHTML = `
    <div class="grid grid-cols-7 gap-1 text-center text-sm font-semibold mb-2">
      ${diasSemana.map(d => `<div>${d.substring(0, 3)}</div>`).join('')}
    </div>
  `;

  const primerDia = new Date(year, month, 1).getDay();
  let html = '<div class="grid grid-cols-7 gap-1 text-sm">';

  for (let i = 0; i < primerDia; i++) {
    html += `<div></div>`;
  }

  for (let dia = 1; dia <= diasMes; dia++) {
    const fecha = new Date(year, month, dia);
    const diaNombre = diasSemana[fecha.getDay()];
    const horario = horarios[diaNombre];

    const hayHorario = horario && (horario.entrada || horario.salida || horario.entrada_2 || horario.salida_2);
    const clases = hayHorario
      ? 'bg-blue-100 hover:bg-blue-200 cursor-pointer'
      : 'text-gray-400';

    html += `
      <div class="p-2 rounded ${clases}"
           data-dia="${dia}"
           data-nombre-dia="${diaNombre}"
           data-horario='${JSON.stringify(horario || {})}'>
        ${dia}
      </div>`;
  }

  html += '</div>';
  calendario.innerHTML += html;

  // Mostrar popup al hacer clic en un día con horario
  calendario.querySelectorAll('[data-dia]').forEach(celda => {
    celda.addEventListener('click', e => {
      const data = JSON.parse(e.currentTarget.dataset.horario || '{}');
      const diaNumero = e.currentTarget.dataset.dia;
      const diaTexto = e.currentTarget.dataset.nombre_dia;

      if (!data.entrada && !data.salida && !data.entrada_2 && !data.salida_2) return;

      const detalles = [];
      if (data.entrada && data.salida) {
        detalles.push(`1er tramo: ${data.entrada} - ${data.salida}`);
      }
      if (data.entrada_2 && data.salida_2) {
        detalles.push(`2º tramo: ${data.entrada_2} - ${data.salida_2}`);
      }

      popup.innerHTML = `
        <div class="font-semibold mb-1">Día ${diaNumero} (${diaTexto})</div>
        ${detalles.join('<br>')}
      `;

      popup.style.top = `${e.clientY + window.scrollY + 12}px`;
      popup.style.left = `${e.clientX}px`;
      popup.classList.remove('hidden');
    });
  });

  // Ocultar popup al hacer clic fuera
  document.addEventListener('click', e => {
    if (!popup.contains(e.target) && !e.target.closest('#calendarioHorario')) {
      popup.classList.add('hidden');
    }
  });
}

// Función auxiliar para reconstruir horarios desde los inputs actuales
export function obtenerHorariosActuales() {
  const dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'];
  const horarios = {};

  dias.forEach(dia => {
    horarios[dia] = {
      entrada: document.querySelector(`[name="${dia}_entrada"]`)?.value || null,
      salida: document.querySelector(`[name="${dia}_salida"]`)?.value || null,
      entrada_2: document.querySelector(`[name="${dia}_entrada_2"]`)?.value || null,
      salida_2: document.querySelector(`[name="${dia}_salida_2"]`)?.value || null,
    };
  });

  return horarios;
}
