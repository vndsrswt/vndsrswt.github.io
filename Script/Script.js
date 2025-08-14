document.getElementById('year').textContent = new Date().getFullYear();

const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
  const currentTheme = document.body.dataset.theme;
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';
  document.body.dataset.theme = newTheme;
  localStorage.setItem('theme', newTheme);
});

// Apply saved theme on page load
const savedTheme = localStorage.getItem('theme') || 'light';
document.body.dataset.theme = savedTheme;