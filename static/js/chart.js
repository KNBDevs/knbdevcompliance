function renderChartFichajes() {
  const ctx = document.getElementById('graficoFichajesSemana');
  if (!ctx) return;

  // Destruye gráfico existente si lo hay
  if (ctx.chartInstance) {
    ctx.chartInstance.destroy();
  }

  const label = window.translations?.dashboard?.chart?.label_fichajes || 'Fichajes';

  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: JSON.parse(ctx.dataset.labels),
      datasets: [{
        label: label,
        data: JSON.parse(ctx.dataset.values),
        borderWidth: 1,
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        borderColor: 'rgba(59, 130, 246, 1)'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });

  // Guarda instancia para poder destruirla luego
  ctx.chartInstance = chart;
}

// Ejecutar al cargar
document.addEventListener('DOMContentLoaded', renderChartFichajes);

// Exponer globalmente
window.renderChartFichajes = renderChartFichajes;
