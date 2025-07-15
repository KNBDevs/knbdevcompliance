// Funciones para mostrar/ocultar el acordeón de acciones
function toggleAcciones(id) {
    const fila = document.getElementById(`acciones-${id}`);
    if (fila) {
        fila.classList.toggle('hidden');
    }
}

function toggleAccionesDesdeElemento(el) {
    const id = el.dataset.id;
    toggleAcciones(id);
}

// Drawer de edición
function cargarDatosEditarCentro(btn) {
    const id = btn.dataset.id;
    document.getElementById('edit-centro-id').value = id;
    document.getElementById('edit-centro-nombre').value = btn.dataset.nombre;
    document.getElementById('edit-centro-empresa').value = btn.dataset.empresa;

    // Nuevos campos (verifica que tengas estos data-* en los botones)
    document.getElementById('edit-centro-email').value = btn.dataset.email || '';
    document.getElementById('edit-centro-telefono').value = btn.dataset.telefono || '';
    document.getElementById('edit-centro-direccion').value = btn.dataset.direccion || '';
    document.getElementById('edit-centro-codigo-postal').value = btn.dataset.codigoPostal || '';
    document.getElementById('edit-centro-ccc').value = btn.dataset.ccc || '';
    document.getElementById('edit-centro-cif').value = btn.dataset.cif || '';
    document.getElementById('edit-centro-responsable').value = btn.dataset.responsable || '';
    document.getElementById('edit-centro-sector').value = btn.dataset.sector || '';
    document.getElementById('edit-centro-fecha').innerText = btn.dataset.fecha || '';

    const form = document.getElementById('formEditarCentro');
    form.action = `/centros/editar/${id}`;

    abrirDrawerEditarCentro();
}


function abrirDrawerEditarCentro() {
    const drawer = document.getElementById('drawerEditarCentro');
    if (drawer) drawer.classList.remove('translate-x-full');
}

function cerrarDrawerEditarCentro() {
    const drawer = document.getElementById('drawerEditarCentro');
    if (drawer) drawer.classList.add('translate-x-full');
}

// Modal de creación
function mostrarModalCentro() {
    const modal = document.getElementById('modalCentro');
    if (modal) modal.classList.remove('hidden');
}

function cerrarModalCentro() {
    const modal = document.getElementById('modalCentro');
    if (modal) modal.classList.add('hidden');
}
