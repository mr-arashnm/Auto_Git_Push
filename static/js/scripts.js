function addPath() {
    const pathInput = document.getElementById('new-path');
    const path = pathInput.value.trim();

    if (!path) {
        alert('Please enter a valid path.');
        return;
    }

    // جمع‌آوری وضعیت عملیات‌ها
    const actions = Array.from(document.querySelectorAll('.action-icon')).map(icon => {
        const action = icon.getAttribute('data-action');
        const isActive = icon.classList.contains('text-blue-500'); // بررسی فعال بودن
        return { action, isActive };
    });

    // ارسال مسیر و وضعیت عملیات‌ها به سرور
    fetch('/save-paths', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path, actions })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        alert('Path and actions saved successfully!');
        loadPaths(); // بارگذاری مجدد مسیرها
    })
    .catch(error => console.error('Error saving path and actions:', error));

    // پاک کردن ورودی
    pathInput.value = '';
}

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
            pathsContainer.innerHTML = ''; // پاک کردن مسیرهای قبلی
            paths.forEach(({ path, is_valid, actions }) => addPathToUI(path, is_valid, actions)); // ارسال اطلاعات عملیات به addPathToUI
        })
        .catch(error => console.error('Error fetching paths:', error));
}

// Add path to UI
function addPathToUI(path, isValid = true, actions = []) {
    const pathsContainer = document.getElementById('paths-container');
    
    const pathItem = document.createElement('div');
    pathItem.className = `path-item bg-gray-50 dark:bg-dark-800 rounded-lg px-4 py-3 flex items-center justify-between border ${isValid ? 'border-gray-200 dark:border-dark-700' : 'border-red-500 dark:border-red-700'}`;
    
    // ایجاد آیکون‌های عملیات
    const actionIcons = actions.map(action => {
        const isActive = true; // فرض کنید همه عملیات‌ها فعال هستند
        const iconClass = isActive
            ? 'text-blue-500 hover:text-blue-600'
            : 'text-gray-400 cursor-not-allowed';
        return `
            <i 
                class="action-icon fas ${getActionIcon(action)} ${iconClass} mx-2"
                data-action="${action}"
                onclick="toggleAction(this)"
                title="${action}"
            ></i>
        `;
    }).join('');

    pathItem.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-file-alt ${isValid ? 'text-green-500' : 'text-red-500'} mr-3"></i>
            <span class="text-gray-700 dark:text-dark-200 font-medium">${path}</span>
        </div>
        <div class="flex items-center space-x-2">
            ${actionIcons}
            <button onclick="removePath(this)" class="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300">
                <i class="fas fa-trash-alt"></i>
            </button>
        </div>
    `;
    
    pathsContainer.appendChild(pathItem);
}

// تابع برای دریافت کلاس آیکون بر اساس نوع عملیات
function getActionIcon(action) {
    return {
        add: 'fa-plus-circle',
        commit: 'fa-check-circle',
        push: 'fa-upload'
    }[action] || 'fa-question-circle';
}

function toggleAction(icon) {
    const action = icon.getAttribute('data-action');
    const isActive = icon.classList.contains('text-blue-500');

    if (isActive) {
        // غیرفعال کردن آیکون
        icon.classList.remove('text-blue-500', 'hover:text-blue-600');
        icon.classList.add('text-gray-400', 'cursor-not-allowed');

        // مدیریت وابستگی‌ها
        if (action === 'add') {
            disableAction('commit');
            disableAction('push');
        } else if (action === 'commit') {
            disableAction('push');
        }
    } else {
        // فعال کردن آیکون
        icon.classList.remove('text-gray-400', 'cursor-not-allowed');
        icon.classList.add('text-blue-500', 'hover:text-blue-600');

        // مدیریت وابستگی‌ها
        if (action === 'add') {
            enableAction('commit');
        } else if (action === 'commit') {
            enableAction('push');
        }
    }
}

function disableAction(action) {
    const icons = document.querySelectorAll(`.action-icon[data-action="${action}"]`);
    icons.forEach(icon => {
        icon.classList.remove('text-blue-500', 'hover:text-blue-600');
        icon.classList.add('text-gray-400', 'cursor-not-allowed');
    });
}

function enableAction(action) {
    const icons = document.querySelectorAll(`.action-icon[data-action="${action}"]`);
    icons.forEach(icon => {
        icon.classList.remove('text-gray-400', 'cursor-not-allowed');
        icon.classList.add('text-blue-500', 'hover:text-blue-600');
    });
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