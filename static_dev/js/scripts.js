// Функция для открытия графика на весь экран
function openFullScreen(imgElement) {
    // Получаем модальное окно
    let modal = document.querySelector('.fullscreen-modal');
    let modalImg = document.querySelector('#fullscreen-img');

    // Устанавливаем источник изображения в модальном окне
    modalImg.src = imgElement.src;

    // Показываем модальное окно
    modal.classList.add('open');
}

// Функция для закрытия модального окна при клике на кнопку
function closeFullScreen() {
    let modal = document.querySelector('.fullscreen-modal');
    modal.classList.remove('open');
}

// Функция для открытия изображения на весь экран
function openFullScreen(image) {
    var modal = document.getElementById("modal");
    var fullScreenImage = document.getElementById("full-screen-image");
    modal.style.display = "block";
    fullScreenImage.src = image.src;
}

// Функция для закрытия модального окна
function closeFullScreen() {
    var modal = document.getElementById("modal");
    modal.style.display = "none";
}

// Открытие модального окна
function openFullScreen(imgElement) {
    // Получаем элемент изображения и отображаем его в модальном окне
    var modal = document.querySelector('.fullscreen-modal');
    var modalImg = document.getElementById("fullscreen-img");
    modal.style.display = "block";
    modalImg.src = imgElement.src; // Устанавливаем src изображения в модальное окно
}

// Закрытие модального окна
function closeFullScreen() {
    var modal = document.querySelector('.fullscreen-modal');
    modal.style.display = "none"; // Скрываем модальное окно
}
