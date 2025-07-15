// ✅ Definir la URL base para los reconocimientos médicos
const urlReconocimientos = '/reconocimientos';

function abrirModalReconocimiento(trabajadorId, nombre) {
    document.getElementById('trabajador-id').value = trabajadorId;
    document.getElementById('nombre-trabajador').textContent = nombre;
    document.getElementById('modal-reconocimiento').classList.remove('hidden');
}

function cerrarModalReconocimiento() {
    document.getElementById('modal-reconocimiento').classList.add('hidden');
}

document.getElementById('form-reconocimiento').addEventListener('submit', async function (e) {
    e.preventDefault();
    const trabajadorId = document.getElementById('trabajador-id').value;
    const fecha = document.getElementById('fecha').value;
    const observaciones = document.getElementById('observaciones').value;

    const response = await fetch(`${urlReconocimientos}/${trabajadorId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fecha, observaciones }),
    });

    if (response.ok) {
        location.reload();
    } else {
        alert('Error al guardar el reconocimiento.');
    }
});

// ✅ Asociar eventos a botones con data-id y data-nombre
document.addEventListener('DOMContentLoaded', () => {
    const botones = document.querySelectorAll('.btn-reconocimiento');

    botones.forEach(boton => {
        boton.addEventListener('click', () => {
            const id = boton.dataset.id;
            const nombre = boton.dataset.nombre;
            abrirModalReconocimiento(id, nombre);
        });
    });
});
