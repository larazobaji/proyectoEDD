document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');

    const setTheme = (isDark) => {
        if (isDark) {
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
            localStorage.setItem('theme', 'light');
        }
    };

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        themeToggle.checked = true;
        setTheme(true);
    } else {
        themeToggle.checked = false;
        setTheme(false);
    }

    themeToggle.addEventListener('change', () => {
        setTheme(themeToggle.checked);
    });

    const composeBtn = document.getElementById('compose-btn');
    const composeModal = document.getElementById('compose-modal');
    const closeBtn = document.getElementById('close-btn');
    const minimizeBtn = document.getElementById('minimize-btn');
    const maximizeBtn = document.getElementById('maximize-btn');
    const composeHeader = composeModal.querySelector('.compose-header');

    let isDragging = false;
    let offsetX, offsetY;

    composeBtn.addEventListener('click', () => {
        composeModal.classList.add('open');
        if (!composeModal.classList.contains('maximized')) {
            composeModal.style.left = '';
            composeModal.style.top = '';
            composeModal.style.transform = 'translateY(0)';
        }
    });

    closeBtn.addEventListener('click', () => {
        composeModal.classList.remove('open', 'maximized');
        composeModal.style.left = '';
        composeModal.style.top = '';
    });

    minimizeBtn.addEventListener('click', () => {
        composeModal.classList.remove('open');
        composeModal.classList.remove('maximized');
        composeModal.style.left = '';
        composeModal.style.top = '';
    });

    maximizeBtn.addEventListener('click', () => {
        composeModal.classList.toggle('maximized');
        if (composeModal.classList.contains('maximized')) {
            composeModal.style.left = '';
            composeModal.style.top = '';
            composeModal.style.transform = '';
        } else {
            composeModal.style.left = '';
            composeModal.style.top = '';
            composeModal.style.transform = 'translateY(0)';
        }
    });

    composeHeader.addEventListener('mousedown', (e) => {
        if (!composeModal.classList.contains('maximized')) {
            isDragging = true;
            composeHeader.classList.add('dragging');
            offsetX = e.clientX - composeModal.getBoundingClientRect().left;
            offsetY = e.clientY - composeModal.getBoundingClientRect().top;
            composeModal.style.transition = 'none';
            composeModal.style.bottom = 'auto';
            composeModal.style.right = 'auto';
        }
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        composeModal.style.left = `${e.clientX - offsetX}px`;
        composeModal.style.top = `${e.clientY - offsetY}px`;
    });

    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            composeHeader.classList.remove('dragging');
            composeModal.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), opacity 0.3s ease';
        }
    });

    const addFolderBtn = document.getElementById('add-folder-btn');
    const folderList = document.getElementById('folder-list');

    addFolderBtn.addEventListener('click', () => {
        const folderName = prompt("Ingresa el nombre de la nueva carpeta:");
        if (folderName && folderName.trim() !== '') {
            const newFolder = document.createElement('li');
            newFolder.innerHTML = `<span class="material-icons">folder</span> ${folderName}`;
            newFolder.classList.add('new-folder');
            folderList.appendChild(newFolder);

            newFolder.addEventListener('click', () => {
                document.querySelectorAll('#folder-list li').forEach(item => {
                    item.classList.remove('active');
                });
                newFolder.classList.add('active');
            });
        }
    });

    folderList.addEventListener('click', (e) => {
        const target = e.target.closest('li');
        if (target && folderList.contains(target)) {
            document.querySelectorAll('#folder-list li').forEach(item => {
                item.classList.remove('active');
            });
            target.classList.add('active');
        }
    });
});