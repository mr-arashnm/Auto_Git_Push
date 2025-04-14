// Save theme to the server
function saveTheme(theme) {
    fetch('/save-theme', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error saving theme:', error));
}


// Load theme from the server
document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-theme')
        .then(response => response.json())
        .then(data => {
            const theme = data.theme || 'dark';
            const html = document.documentElement;
            const themeIcon = document.getElementById('theme-icon');

            if (theme === 'dark') {light
                html.classList.add('dark');
                themeIcon.classList.replace('fa-moon', 'fa-sun');
            } else {
                html.classList.remove('dark');
                themeIcon.classList.replace('fa-sun', 'fa-moon');
            }
        })
        .catch(error => console.error('Error fetching theme:', error));
});


// Load paths from the server and display them
document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-paths')
        .then(response => response.json())
        .then(paths => {
            const pathsContainer = document.getElementById('paths-container');
            pathsContainer.innerHTML = ''; // Clear existing paths

            paths.forEach(({ path, isValid }) => {
                addPathToUI(path, isValid);
            });
        })
        .catch(error => console.error('Error fetching paths:', error));
});

// Add a path to the UI with validation status
function addPathToUI(path, isValid) {
    const pathsContainer = document.getElementById('paths-container');

    const pathItem = document.createElement('div');
    pathItem.className = 'path-item bg-gray-50 dark:bg-dark-800 rounded-lg px-4 py-3 flex items-center justify-between border border-gray-200 dark:border-dark-700';
    pathItem.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-file-alt text-green-500 mr-3"></i>
            <span class="text-gray-700 dark:text-dark-200 font-medium">${path}</span>
        </div>
        <div class="flex items-center">
            ${isValid ? '<i class="fas fa-check-circle text-green-500"></i>' : '<i class="fas fa-times-circle text-red-500"></i>'}
            <button onclick="removePath(this)" class="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 ml-4">
                <i class="fas fa-trash-alt"></i>
            </button>
        </div>
    `;

    pathsContainer.appendChild(pathItem);
}

// Validate a path by sending a request to the server
function validatePath(path) {
    return fetch('/validate-path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path })
    })
    .then(response => response.json())
    .then(data => data.isValid)
    .catch(error => {
        console.error('Error validating path:', error);
        return false;
    });
}

// Add a path to the UI with validation status
function addPathToUI(path, isValid) {
    const pathsContainer = document.getElementById('paths-container');

    const pathItem = document.createElement('div');
    pathItem.className = 'path-item bg-gray-50 dark:bg-dark-800 rounded-lg px-4 py-3 flex items-center justify-between border border-gray-200 dark:border-dark-700';
    pathItem.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-file-alt text-green-500 mr-3"></i>
            <span class="text-gray-700 dark:text-dark-200 font-medium">${path}</span>
        </div>
        <div class="flex items-center">
            ${isValid ? '<i class="fas fa-check-circle text-green-500"></i>' : '<i class="fas fa-times-circle text-red-500"></i>'}
            <button onclick="removePath(this)" class="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 ml-4">
                <i class="fas fa-trash-alt"></i>
            </button>
        </div>
    `;

    pathsContainer.appendChild(pathItem);
}

// Theme toggle functionality
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const html = document.documentElement;

// Check for saved theme preference or use system preference
if (localStorage.getItem('theme') === 'dark' || 
    (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    html.classList.add('dark');
    themeIcon.classList.replace('fa-moon', 'fa-sun');
} else {
    html.classList.remove('dark');
    themeIcon.classList.replace('fa-sun', 'fa-moon');
}

// Toggle theme
themeToggle.addEventListener('click', () => {
    html.classList.toggle('dark');
    if (html.classList.contains('dark')) {
        localStorage.setItem('theme', 'dark');
        themeIcon.classList.replace('fa-moon', 'fa-sun');
    } else {
        localStorage.setItem('theme', 'light');
        themeIcon.classList.replace('fa-sun', 'fa-moon');
    }
});