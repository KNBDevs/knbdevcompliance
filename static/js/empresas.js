// Mostrar/Ocultar acordeón
function toggleAcciones(id) {
    const fila = document.getElementById(`acciones-${id}`);
    if (fila) fila.classList.toggle('hidden');
}

function toggleAccionesDesdeElemento(el) {
    const id = el.dataset.id;
    toggleAcciones(id);
}

// Drawer de edición
function cargarDatosEditarEmpresa(btn) {
    console.log("Editando empresa", btn.dataset.id);

    const id = btn.dataset.id;
    document.getElementById('edit-empresa-id').value = id;
    document.getElementById('edit-empresa-nombre').value = btn.dataset.nombre;
    document.getElementById('edit-empresa-cif').value = btn.dataset.cif;
    document.getElementById('edit-empresa-ccc').value = btn.dataset.ccc;
    document.getElementById('edit-empresa-contacto').value = btn.dataset.contacto || '';
    document.getElementById('edit-empresa-administrador').value = btn.dataset.administrador || '';
    document.getElementById('edit-empresa-telefono').value = btn.dataset.telefono || '';
    document.getElementById('edit-empresa-email').value = btn.dataset.email || '';
    document.getElementById('edit-empresa-sede-fiscal').value = btn.dataset.sede_fiscal || '';
    document.getElementById('edit-empresa-codigo-postal').value = btn.dataset.codigo_postal || '';
    document.getElementById('edit-empresa-iban').value = btn.dataset.iban || '';

    const form = document.getElementById('formEditarEmpresa');
    form.action = `/empresas/editar/${id}`;

    abrirDrawerEditarEmpresa();
}

function abrirDrawerEditarEmpresa() {
    document.getElementById('drawerEditarEmpresa').classList.remove('translate-x-full');
}

function cerrarDrawerEditarEmpresa() {
    document.getElementById('drawerEditarEmpresa').classList.add('translate-x-full');
}

// Modal nueva empresa
function mostrarModalEmpresa() {
    document.getElementById('modalEmpresa').classList.remove('hidden');
}

function cerrarModalEmpresa() {
    document.getElementById('modalEmpresa').classList.add('hidden');
}

// Opcional: imprimir URL al enviar el formulario
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formEditarEmpresa');
    if (form) {
        form.addEventListener('submit', (e) => {
            console.log("Formulario enviado a:", form.action);
        });
    }
});
