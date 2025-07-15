// Mostrar y ocultar acciones (acordeón)
function toggleAcciones(id) {
    const fila = document.getElementById(`acciones-${id}`);
    if (fila) fila.classList.toggle('hidden');
}

function toggleAccionesDesdeElemento(el) {
    const id = el.dataset.id;
    toggleAcciones(id);
}

// Modal de creación
function mostrarModalCrear() {
    const modal = document.getElementById('modalTrabajador');
    if (modal) modal.classList.remove('hidden');
}

function cerrarModalCrear() {
    const modal = document.getElementById('modalTrabajador');
    if (modal) modal.classList.add('hidden');
}

// Drawer de edición
function abrirDrawerEditar() {
    const drawer = document.getElementById('drawerEditar');
    if (drawer) drawer.classList.remove('translate-x-full');
}

function cerrarDrawerEditar() {
    const drawer = document.getElementById('drawerEditar');
    if (drawer) drawer.classList.add('translate-x-full');
}

// Cargar datos en el drawer
function cargarDatosEditar(btn) {
    const id = btn.dataset.id;
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-nombre').value = btn.dataset.nombre;
    document.getElementById('edit-email').value = btn.dataset.email;
    document.getElementById('edit-telefono').value = btn.dataset.telefono;
    document.getElementById('edit-dni').value = btn.dataset.dni;
    document.getElementById('edit-centro_id').value = btn.dataset.centro || '';
    document.getElementById('edit-nacionalidad').value = btn.dataset.nacionalidad || '';
    document.getElementById('edit-genero').value = btn.dataset.genero || '';

    const form = document.getElementById('formEditarTrabajador');
    form.action = `/trabajadores/editar/${id}`;

    abrirDrawerEditar();
}


// Cierre con ESC
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        cerrarModalCrear();
        cerrarDrawerEditar();
    }
});

// Cierre al hacer clic fuera
document.addEventListener('click', function (e) {
    const modal = document.getElementById('modalTrabajador');
    const drawer = document.getElementById('drawerEditar');

    // Modal: cerrar si está abierto y se hace clic fuera del contenido
    if (modal && !modal.classList.contains('hidden') &&
        !modal.querySelector('form').contains(e.target) &&
        !e.target.closest('[onclick="mostrarModalCrear()"]')) {
        cerrarModalCrear();
    }

    // Drawer: cerrar si está abierto y se hace clic fuera
    if (drawer && !drawer.classList.contains('translate-x-full') &&
        !drawer.contains(e.target) &&
        !e.target.closest('[onclick^="cargarDatosEditar"]')) {
        cerrarDrawerEditar();
    }
});


// Comportamiento exclusivo entre "Mostrar eliminados" y "Solo sin centro"
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('filtros-trabajadores');
    if (!form) return;

    const chkEliminados = form.querySelector('input[name="eliminados"]');
    const chkHuerfanos = form.querySelector('input[name="huerfanos"]');

    if (chkEliminados && chkHuerfanos) {
        chkEliminados.addEventListener('change', function () {
            if (this.checked) {
                // Redirige a una URL limpia solo con ?eliminados=1
                const url = new URL(form.action, window.location.origin);
                url.search = '?eliminados=1';
                window.location.href = url.toString();
            }
        });

        chkHuerfanos.addEventListener('change', function () {
            if (this.checked) {
                // Redirige directamente a la vista exclusiva
                window.location.href = '/trabajadores/sin_centro';
            }
        });
    }
});


function accionTrabajador(select) {
    const trabajadorId = select.dataset.trabajadorId;
    const accion = select.value;

    if (!accion || !trabajadorId) return;

    switch (accion) {
        case 'horario':
            window.location.href = `/horarios/${trabajadorId}`;
            break;
        case 'fichajes':
            window.location.href = `/fichajes/${trabajadorId}`;
            break;
        case 'permiso':
            window.location.href = `/permisos/${trabajadorId}`;
            break;
        case 'formacion':
            abrirModalCursos(trabajadorId);
            break;
        case 'reconocimiento':
            window.location.href = `/reconocimientos/trabajador/${trabajadorId}`;
            break;
    }
}


function abrirModalCurso(trabajadorId) {
    const modal = document.getElementById('modal-curso');
    const inputId = document.getElementById('trabajador-id');
    const listaCursos = document.getElementById('lista-cursos');

    if (!modal || !inputId || !listaCursos) return;

    // Establecer ID del trabajador
    inputId.value = trabajadorId;

    // Limpiar cursos previos por si acaso
    listaCursos.innerHTML = '';

    // Aquí puedes cargar cursos dinámicamente con AJAX si lo deseas
    // Por ahora simplemente muestra el modal
    modal.classList.remove('hidden');
}


function cerrarModalCursos() {
    const modal = document.getElementById('modal-curso');
    if (modal) modal.classList.add('hidden');
}


// Filtro de trabajadores en tiempo real (nombre, email o teléfono)
function filtrarTrabajadores() {
    const filtro = document.getElementById("buscador-trabajador").value.toLowerCase();
    const filas = document.querySelectorAll("tbody tr:not([id^='acciones-'])");

    filas.forEach(fila => {
        const nombre = fila.querySelector("td:nth-child(1)").innerText.toLowerCase();
        const email = fila.querySelector("td:nth-child(2)").innerText.toLowerCase();
        const telefono = fila.querySelector("td:nth-child(3)").innerText.toLowerCase();

        const coincide = nombre.includes(filtro) || email.includes(filtro) || telefono.includes(filtro);
        fila.style.display = coincide ? "" : "none";

        const id = fila.dataset.id;
        const acordeon = document.getElementById("acciones-" + id);
        if (acordeon) {
            acordeon.style.display = coincide ? "" : "none";
        }
    });
}
