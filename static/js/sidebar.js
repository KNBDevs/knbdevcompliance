document.addEventListener('DOMContentLoaded', function () {
  const toggleButton = document.getElementById('sidebarToggle');
  const closeButton = document.getElementById('sidebarClose');
  const sidebar = document.getElementById('mobileSidebar');

  function isMobile() {
    return window.innerWidth < 768;
  }

  function openSidebar() {
    sidebar.classList.remove('-translate-x-full');
    sidebar.classList.add('translate-x-0');
  }

  function closeSidebar() {
    sidebar.classList.add('-translate-x-full');
    sidebar.classList.remove('translate-x-0');
  }

  if (!sidebar || !toggleButton || !closeButton) return;

  toggleButton.addEventListener('click', () => {
    if (sidebar.classList.contains('-translate-x-full')) {
      openSidebar();
    } else {
      closeSidebar();
    }
  });

  closeButton.addEventListener('click', () => {
    closeSidebar();
  });

  // Al cambiar de tamaño de ventana, forzar estado cerrado si pasamos a escritorio
  window.addEventListener('resize', () => {
    if (!isMobile()) {
      closeSidebar();
    }
  });
});
