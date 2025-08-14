// Theme Toggle
document.getElementById("theme-toggle").addEventListener("click", function() {
    document.body.classList.toggle("dark-theme");
    document.body.classList.toggle("light-theme");
    const theme = document.body.classList.contains("dark-theme") ? "dark" : "light";
    localStorage.setItem("theme", theme);
});

// Load Saved Theme
const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
    document.body.classList.remove("light-theme", "dark-theme");
    document.body.classList.add(savedTheme + "-theme");
}
