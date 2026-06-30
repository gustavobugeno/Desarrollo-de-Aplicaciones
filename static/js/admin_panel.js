console.log("✅ admin_panel.js cargado correctamente");

// Resaltar enlace activo
document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".sidebar a");
    const currentUrl = window.location.pathname;

    links.forEach(link => {
        if (link.getAttribute("href") === currentUrl) {
            link.style.backgroundColor = "#00bcd4";
            link.style.color = "#fff";
        }
    });
});
