// Save telegram settings
function saveTelegramSettings() {
    const telegramChatId = document.getElementById('telegram-id').value.trim();
    const notificationsEnabled = document.getElementById('telegram-toggle').checked;

    fetch('/telegram-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            telegram_chat_id: telegramChatId,
            notifications_enabled: notificationsEnabled
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error saving telegram settings:', error));
}

// Save email settings
function saveEmailSettings() {
    const emailUsername = document.getElementById('email').value.trim();
    const notificationsEnabled = document.getElementById('email-toggle').checked;

    fetch('/email-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email_username: emailUsername,
            notifications_enabled: notificationsEnabled
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error saving email settings:', error));
}

const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

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

function removePath(button) {
    const pathItem = button.closest('.path-item');
    pathItem.classList.add('opacity-0', 'scale-95');
    
    setTimeout(() => {
        pathItem.remove();
    }, 200);
}

function getTheme() {
    fetch('/get-theme')
        .then(response => response.json())
        .then(data => {
            const theme = data.theme || 'dark'; 
            const html = document.documentElement;

            // اعمال تم
            if (theme === 'dark') {
                html.classList.add('dark');
            } else {
                html.classList.remove('dark');
            }

            console.log(`Current theme: ${theme}`);
        })
        .catch(error => console.error('Error fetching theme:', error));
}

// Save theme
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

// Load paths
function loadPaths() {
    fetch('/get-paths')
        .then(response => response.json())
        .then(paths => {
            const pathsContainer = document.getElementById('paths-container');
            pathsContainer.innerHTML = '';
            paths.forEach(({ path, isValid }) => addPathToUI(path, isValid));
        })
        .catch(error => console.error('Error fetching paths:', error));
}

// Add path to UI
function addPathToUI(path) {
    const pathsContainer = document.getElementById('paths-container');
    
    const pathItem = document.createElement('div');
    pathItem.className = 'path-item bg-gray-50 dark:bg-dark-800 rounded-lg px-4 py-3 flex items-center justify-between border border-gray-200 dark:border-dark-700';
    pathItem.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-file-alt text-green-500 mr-3"></i>
            <span class="text-gray-700 dark:text-dark-200 font-medium">${path}</span>
        </div>
        <button onclick="removePath(this)" class="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300">
            <i class="fas fa-trash-alt"></i>
        </button>
    `;
    
    pathsContainer.appendChild(pathItem);
}

// Remove path
function removePath(button) {
    const pathItem = button.closest('.path-item');
    const path = pathItem.querySelector('span').textContent;
    pathItem.remove();

    const paths = Array.from(document.querySelectorAll('.path-item span')).map(el => el.textContent);
    fetch('/save-paths', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ paths })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error saving paths:', error));
}

// Load telegram settings
function loadTelegramSettings() {
    fetch('/telegram-settings')
        .then(response => response.json())
        .then(data => {
            document.getElementById('telegram-id').value = data.telegram_chat_id || '';
            document.getElementById('telegram-toggle').checked = data.notifications_enabled || false;
        })
        .catch(error => console.error('Error fetching telegram settings:', error));
}

// Load email settings
function loadEmailSettings() {
    fetch('/email-settings')
        .then(response => response.json())
        .then(data => {
            document.getElementById('email').value = data.email_username || '';
            document.getElementById('email-toggle').checked = data.notifications_enabled || false;
        })
        .catch(error => console.error('Error fetching email settings:', error));
}

// Load theme
function loadTheme() {
    const theme = localStorage.getItem('theme') || 'dark';
    document.documentElement.classList.toggle('dark', theme === 'dark');
    themeIcon.classList.toggle('fa-sun', theme === 'dark');
    themeIcon.classList.toggle('fa-moon', theme !== 'dark');
}
// Load theme on page load
document.addEventListener('DOMContentLoaded', function () {
    loadTheme();
    getTheme();
});

// Load settings on page load
document.addEventListener('DOMContentLoaded', function () {
    loadPaths();
    loadTelegramSettings();
    loadEmailSettings();
});