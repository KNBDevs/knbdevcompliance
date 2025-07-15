document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggleAccordion');
    const content = document.getElementById('accordionContent');
    const icon = document.getElementById('accordionIcon');
    const storageKey = 'accordionOpen';

    if (!toggleButton || !content || !icon) return;

    const isOpen = localStorage.getItem(storageKey) === 'true';

    // Evitar animación en carga
    if (isOpen) {
        content.classList.remove('hidden');
        content.classList.remove('transition-all', 'duration-300'); // Desactiva animación
        content.style.maxHeight = 'none'; // Sin animación, altura automática
        icon.classList.add('rotate-180');
    } else {
        content.style.maxHeight = '0px';
        icon.classList.remove('rotate-180');
    }

    // Función para expandir con animación
    function expandAccordion() {
        content.classList.add('transition-all', 'duration-300'); // Asegura que tenga animación ahora
        content.style.maxHeight = content.scrollHeight + 'px';
        icon.classList.add('rotate-180');
    }

    // Función para colapsar con animación
    function collapseAccordion() {
        content.classList.add('transition-all', 'duration-300');
        content.style.maxHeight = '0px';
        icon.classList.remove('rotate-180');
    }

    // Toggle manual
    toggleButton.addEventListener('click', () => {
        const isExpanded = content.style.maxHeight !== '0px' && content.style.maxHeight !== '';
        if (isExpanded) {
            collapseAccordion();
            localStorage.setItem(storageKey, 'false');
        } else {
            expandAccordion();
            localStorage.setItem(storageKey, 'true');
        }
    });
});
