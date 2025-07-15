function filtrarCentro() {
    const centroId = document.getElementById("centro-select").value;
    const filas = document.querySelectorAll("#tabla-trabajadores tbody tr");

    filas.forEach(fila => {
        const centroFila = fila.getAttribute("data-centro");
        fila.style.display = (!centroId || centroId === centroFila) ? "" : "none";
    });
}
