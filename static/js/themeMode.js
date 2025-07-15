document.addEventListener('DOMContentLoaded', () => {
    const modeSelector = document.getElementById('modeSelector');
    const root = document.documentElement;

    if (!modeSelector) return;

    // Estado inicial: aplicar el modo guardado
    const savedMode = sessionStorage.getItem('displayMode') || 'light';
    modeSelector.value = savedMode;
    applyMode(savedMode);

    // Al cambiar la opción del selector
    modeSelector.addEventListener('change', () => {
        const selectedMode = modeSelector.value;
        sessionStorage.setItem('displayMode', selectedMode);
        applyMode(selectedMode);
    });

    function applyMode(mode) {
        root.classList.remove('dark', 'tired-mode');
        if (mode === 'dark') {
            root.classList.add('dark');
        } else if (mode === 'tired') {
            root.classList.add('tired-mode');
        }
        // No se necesita acción para "light"
    }
});
