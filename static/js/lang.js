async function loadLanguage(lang) {
    try {
        const response = await fetch(`/static/lang/${lang}.json`);
        const translations = await response.json();

        // ⚠️ GUARDAR ANTES DE USAR
        window.translations = translations;

        // Traducción de elementos estáticos
        document.querySelectorAll('[data-i18n]').forEach(elem => {
            const key = elem.getAttribute('data-i18n');
            const rawParams = elem.getAttribute('data-i18n-params');
            const text = resolveNestedKey(translations, key);

            if (text) {
                if (rawParams) {
                    try {
                        const params = JSON.parse(rawParams);
                        elem.innerText = interpolate(text, params);
                    } catch (e) {
                        console.warn(`Error al parsear data-i18n-params para ${key}:`, e);
                        elem.innerText = text;
                    }
                } else {
                    elem.innerText = text;
                }
            }
        });


        // Traducción de placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(elem => {
            const key = elem.getAttribute('data-i18n-placeholder');
            const text = resolveNestedKey(translations, key);
            if (text) elem.setAttribute('placeholder', text);
        });



        // ✅ Solo aquí después de guardar translations
        if (typeof window.renderChartFichajes === 'function') {
            window.renderChartFichajes();
        }


        // Forzar traducción de elementos dinámicos tras cargar idioma
        const archivoLabel = document.getElementById('archivo-label');
        const archivoNombre = document.getElementById('archivo-nombre');

        if (archivoLabel) {
            const labelText = resolveNestedKey(translations, 'importar_trabajadores.boton_archivo');
            if (labelText) archivoLabel.textContent = labelText;
            else archivoLabel.textContent = 'Seleccionar archivo'; // fallback
        }

        if (archivoNombre) {
            const nombreText = resolveNestedKey(translations, 'importar_trabajadores.no_seleccionado');
            if (nombreText && !archivoNombre.textContent.trim()) {
                archivoNombre.textContent = nombreText;
            }
        }

        document.documentElement.lang = lang;

        // ✅ Mostrar modal de fichaje SOLO DESPUÉS de cargar el idioma
        const params = new URLSearchParams(window.location.search);
        const tipo = params.get('fichaje');
        if (tipo && translations?.fichaje_modal?.[tipo]) {
            const nombre = decodeURIComponent(params.get('nombre') || '');
            const hora = params.get('hora') || '';

            const data = translations.fichaje_modal[tipo];

            const titulo = interpolate(data.titulo, { nombre, hora });
            const mensaje = interpolate(data.mensaje, { nombre, hora });

            const modal = document.getElementById('fichajeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalMessage = document.getElementById('modalMessage');
            const modalButton = document.getElementById('modalOkButton');

            if (modal && modalTitle && modalMessage) {
                modalTitle.innerText = titulo;
                modalMessage.innerText = mensaje;
                if (modalButton && translations?.login?.ok) {
                    modalButton.innerText = translations.login.ok;
                }
                modal.classList.remove('hidden');
            }
        }

    } catch (error) {
        console.error(`Error cargando idioma "${lang}":`, error);
    }
}

// Función para resolver claves anidadas como "login.title"
function resolveNestedKey(obj, key) {
    return key.split('.').reduce((o, i) => (o ? o[i] : undefined), obj);
}

// Reemplaza {param} en el texto con los valores pasados
function interpolate(template, params) {
    return template.replace(/{(.*?)}/g, (_, key) => {
        return params[key] ?? `{${key}}`;
    });
}

window.changeLanguage = function (lang) {
    sessionStorage.setItem('lang', lang);
    loadLanguage(lang);
};

document.addEventListener('DOMContentLoaded', () => {
    const lang = sessionStorage.getItem('lang') || 'es';
    const selector = document.getElementById('langSelector');
    if (selector) selector.value = lang;
    loadLanguage(lang);

    // 🎯 Traducción dinámica del nombre del archivo seleccionado
    const inputArchivo = document.getElementById('archivo');
    const textoNombre = document.getElementById('archivo-nombre');

    if (inputArchivo && textoNombre) {
        inputArchivo.addEventListener('change', function () {
            const defaultText = resolveNestedKey(window.translations, 'importar_trabajadores.no_seleccionado') || 'Ningún archivo seleccionado';
            textoNombre.textContent = this.files[0]?.name || defaultText;
        });
    }
});
