document.addEventListener('DOMContentLoaded', () => {
    const langBtn = document.getElementById('langBtn');
    const langMenu = document.getElementById('langMenu');
    const currentFlag = document.getElementById('currentFlag');

    if (!langBtn || !langMenu || !currentFlag) return;

    // Mostrar/ocultar el menú al hacer clic
    langBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        langMenu.classList.toggle('hidden');
    });

    // Cerrar el menú si se hace clic fuera
    document.addEventListener('click', (e) => {
        if (!langMenu.contains(e.target) && !langBtn.contains(e.target)) {
            langMenu.classList.add('hidden');
        }
    });

    // Cambiar idioma al seleccionar una opción
    langMenu.querySelectorAll('[data-lang]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const lang = link.getAttribute('data-lang');
            sessionStorage.setItem('lang', lang);
            changeLanguage(lang);
            currentFlag.src = `/static/img/flags/${lang}.png`;
            langMenu.classList.add('hidden');
        });
    });

    // Establecer bandera al cargar según sessionStorage
    const savedLang = sessionStorage.getItem('lang') || 'es';
    currentFlag.src = `/static/img/flags/${savedLang}.png`;
});
