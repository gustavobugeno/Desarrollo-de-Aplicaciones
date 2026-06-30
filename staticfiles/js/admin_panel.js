// ✅ Archivo cargado correctamente
console.log("admin_panel.js cargado correctamente");

// Animación simple para el sidebar
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const links = sidebar.querySelectorAll("a");

    links.forEach(link => {
        link.addEventListener("mouseenter", () => {
            link.style.backgroundColor = "#007bff";
            link.style.color = "white";
            link.style.transition = "0.3s";
        });

        link.addEventListener("mouseleave", () => {
            link.style.backgroundColor = "transparent";
            link.style.color = "#333";
        });
    });
});
