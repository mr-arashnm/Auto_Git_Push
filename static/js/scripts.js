
// Save accounts (Telegram and Email) to the server
function saveAccounts() {
    const telegramChatId = document.getElementById('telegram-id').value.trim();
    const emailUsername = document.getElementById('email').value.trim();

    fetch('/save-accounts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            telegram_chat_id: telegramChatId,
            email_username: emailUsername
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error saving accounts:', error));
}

// Load accounts (Telegram and Email) from the server
document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-accounts')
        .then(response => response.json())
        .then(data => {
            document.getElementById('telegram-id').value = data.telegram_chat_id || '';
            document.getElementById('email').value = data.email_username || '';
        })
        .catch(error => console.error('Error fetching accounts:', error));
});

// Save telegram notifications status to the server
document.getElementById('telegram-toggle').addEventListener('change', function () {
    const enabled = this.checked;

    fetch('/save-telegram-notifications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error saving telegram notifications:', error));
});

// Load telegram notifications status from the server
document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-telegram-notifications')
        .then(response => response.json())
        .then(data => {
            const telegramToggle = document.getElementById('telegram-toggle');
            telegramToggle.checked = data.enabled;
        })
        .catch(error => console.error('Error fetching telegram notifications status:', error));
});

// Remove a path from the UI and update the server
function removePath(button) {
    const pathItem = button.closest('.path-item');
    const path = pathItem.querySelector('span').textContent;

    // Remove the path from the UI
    pathItem.remove();

    // Update the server with the new list of paths
    const pathElements = document.querySelectorAll('#paths-container .path-item span');
    const paths = Array.from(pathElements).map(el => el.textContent);

    fetch('/save-paths', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ paths })
    })
    .then(response => {
        if (response.ok) {
            console.log(`Path "${path}" removed successfully.`);
        } else {
            console.error(`Failed to remove path "${path}".`);
        }
    })
    .catch(error => console.error('Error updating paths:', error));
}

// Save email notifications status to the server
document.getElementById('email-toggle').addEventListener('change', function () {
    const enabled = this.checked;

    fetch('/save-email-notifications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error saving email notifications:', error));
});

// Load email notifications status from the server
document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-email-notifications')
        .then(response => response.json())
        .then(data => {
            const emailToggle = document.getElementById('email-toggle');
            emailToggle.checked = data.enabled;
        })
        .catch(error => console.error('Error fetching email notifications status:', error));
});

// Add a new path when Enter is pressed
document.getElementById('new-path').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // جلوگیری از رفتار پیش‌فرض (مثل ارسال فرم)
        addPath();
    }
});

// Add a new path
function addPath() {
    const pathInput = document.getElementById('new-path');
    const path = pathInput.value.trim();

    if (path) {
        addPathToUI(path, false); // فرض می‌کنیم مسیر جدید هنوز ولید نیست
        pathInput.value = ''; // پاک کردن فیلد ورودی
    }
}

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
            const theme = data.theme || 'light';
            const html = document.documentElement;
            const themeIcon = document.getElementById('theme-icon');

            if (theme === 'dark') {
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