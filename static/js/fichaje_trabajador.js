
function mostrarModal(titulo, mensaje, tipo = "info") {
    const modal = document.getElementById('fichajeModal');
    const titleEl = document.getElementById('modalTitle');
    const messageEl = document.getElementById('modalMessage');
    const buttonEl = document.getElementById('modalOkButton');

    // Limpiar clases previas
    modal.className = "fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50";
    const modalBox = modal.querySelector('div');

    modalBox.className = "rounded-lg p-6 shadow-md max-w-sm text-center";

    // Estilo según tipo
    if (tipo === "success") {
        modalBox.classList.add("bg-green-100", "text-green-900", "dark:bg-green-800", "dark:text-green-100");
        buttonEl.className = "mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700";
    } else if (tipo === "error") {
        modalBox.classList.add("bg-red-100", "text-red-900", "dark:bg-red-800", "dark:text-red-100");
        buttonEl.className = "mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700";
    } else if (tipo === "warning") {
        modalBox.classList.add("bg-yellow-100", "text-yellow-900", "dark:bg-yellow-800", "dark:text-yellow-100");
        buttonEl.className = "mt-4 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600";
    } else {
        modalBox.classList.add("bg-white", "dark:bg-gray-800");
        buttonEl.className = "mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700";
    }

    titleEl.innerText = titulo;
    messageEl.innerText = mensaje;
    modal.classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('fichajeModal').classList.add('hidden');
    window.location.href = loginUrl;
}

document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const fichaje = params.get("fichaje");

    if (fichaje === "ok") {
        const nombre = decodeURIComponent(params.get("nombre") || "");
        const hora = params.get("hora") || "";
        const tipo = params.get("tipo") || "";
        const entrada = params.get("entrada") || "";
        const salida = params.get("salida") || "";

        const mensaje = (!entrada && !salida)
            ? `${nombre} ha fichado su ${tipo} a las ${hora}.\n\nTurno libre.`
            : `${nombre} ha fichado su ${tipo} a las ${hora}.\n\nTurno: ${entrada} - ${salida}`;

        mostrarModal("✅ Fichaje exitoso", mensaje, "success");

    } else if (fichaje === "error") {
        mostrarModal("❌ Error", "No se encontró un trabajador con ese PIN.", "error");

    } else if (fichaje === "ya_fichado") {
        const nombre = decodeURIComponent(params.get("nombre") || "");
        mostrarModal("⚠️ Ya fichado", `${nombre} ya ha registrado fichaje hoy.`, "warning");

    } else if (fichaje === "demasiado_pronto") {
        const nombre = decodeURIComponent(params.get("nombre") || "");
        mostrarModal("⏱️ Demasiado pronto", `${nombre}, aún no puedes fichar. Espera al inicio del turno.`, "error");
    } else if (fichaje === "demasiado_tarde") {
        const nombre = decodeURIComponent(params.get("nombre") || "");
        mostrarModal("⏱️ Fuera de horario", `${nombre}, ya terminó tu turno. No puedes fichar ahora.`, "error");
    } else if (fichaje === "segundo_turno") {
        const nombre = decodeURIComponent(params.get("nombre") || "");
        const hora = params.get("hora") || "";
        const tipo = params.get("tipo") || "";
        mostrarModal("⚠️ Segundo turno", `${nombre} ha fichado su ${tipo} a las ${hora}.`, "warning");
    } else if (fichaje === "limite_turnos") {
        const nombre = decodeURIComponent(params.get("nombre") || "");
        mostrarModal("❌ Límite alcanzado", `${nombre}, ya has fichado dos turnos hoy.`, "error");
    }


    document.getElementById('toggleAdminLogin').addEventListener('click', () => {
        document.getElementById('adminLoginForm').classList.toggle('hidden');
    });

    const dniInput = document.getElementById('dni5');
    if (dniInput) {
        dniInput.addEventListener('input', function () {
            if (this.value.length === 5) {
                document.getElementById('fichajeForm').submit();
            }
        });
    }
});
