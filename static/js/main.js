// Funciones generales para la aplicación

// Función para cerrar automáticamente las alertas después de 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    // Auto-cerrar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-warning)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });

    // Activar todos los tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
