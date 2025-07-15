async function abrirModalCursos(trabajadorId) {
    document.getElementById('modal-curso').classList.remove('hidden');
    document.getElementById('trabajador-id').value = trabajadorId;

    try {
        const response = await fetch(`/prevencion/cursos/${trabajadorId}`);
        const cursos = await response.json();

        const container = document.getElementById('lista-cursos');
        container.innerHTML = '';

        cursos.todos.forEach(curso => {
            const checked = cursos.asignados.includes(curso.id) ? 'checked' : '';
            container.innerHTML += `
                <label class="flex items-center gap-2">
                    <input type="checkbox" name="cursos" value="${curso.id}" ${checked} />
                    <span>${curso.icono || ''} ${curso.nombre}</span>
                </label>`;
        });
    } catch (error) {
        alert(window.translations?.formacion?.errores?.cargar || "Error al cargar los cursos");
        console.error(error);
    }
}

function cerrarModalCursos() {
    document.getElementById('modal-curso').classList.add('hidden');
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('form-cursos');
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const trabajadorId = document.getElementById('trabajador-id').value;
            const checkboxes = document.querySelectorAll('input[name="cursos"]:checked');
            const cursoIds = Array.from(checkboxes).map(cb => cb.value);

            try {
                await fetch(`/prevencion/cursos/${trabajadorId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cursos: cursoIds })
                });

                location.reload(); // Refresca para actualizar iconos
            } catch (error) {
                alert(window.translations?.formacion?.errores?.guardar || "Error al guardar los cursos");
                console.error(error);
            }
        });
    }
});
