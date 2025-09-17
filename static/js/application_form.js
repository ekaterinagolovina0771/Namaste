// Ждем, пока весь HTML-документ будет загружен и разобран.
// Это стандартная практика, чтобы гарантировать, что все DOM-элементы доступны для манипуляций.
document.addEventListener("DOMContentLoaded", function () {
  // Находим выпадающий список инструкторов и контейнер для чекбоксов практик по их ID.
  const coachSelect = document.getElementById("id_coach");
  const schedulesContainer = document.getElementById("schedules-container");

  // Выполняем код, только если оба элемента найдены на странице.
  if (coachSelect && schedulesContainer) {
    // Добавляем обработчик события, который сработает каждый раз, когда пользователь меняет выбранного инструктора.
    coachSelect.addEventListener("change", function () {
      // Получаем ID выбранного инструктора. 'this.value' ссылается на атрибут 'value' выбранного <option>.
      const coachId = this.value;

      // Если пользователь выбрал "пустой" вариант (например, "Выберите инструктора..."), у которого нет value,
      // очищаем список практик и показываем подсказку.
      if (!coachId) {
        schedulesContainer.innerHTML =
          '<p class="text-muted">Выберите инструктора, чтобы увидеть список практик.</p>';
        return; // Прекращаем дальнейшее выполнение функции.
      }

      // Формируем URL для нашего API-эндпоинта. ID инструктора добавляется к базовому URL.
      const url = `/ajax/schedules/${coachId}/`;

      // Используем современный Fetch API для выполнения асинхронного GET-запроса на сервер.
      fetch(url)
        .then((response) => {
          // Проверяем, успешен ли HTTP-ответ (статус в диапазоне 200-299).
          if (!response.ok) {
            // Если нет, создаем ошибку, которая будет перехвачена блоком .catch().
            throw new Error("Network response was not ok");
          }
          // Парсим JSON-тело ответа. Этот метод также возвращает Promise.
          return response.json();
        })
        .then((data) => {
          // Этот блок выполняется, когда JSON-данные успешно распарсены.
          // Сначала полностью очищаем контейнер от старых чекбоксов.
          schedulesContainer.innerHTML = "";

          // Проверяем, есть ли в ответе практики и не пустой ли массив.
          if (data.schedules && data.schedules.length > 0) {
            // Проходимся в цикле по каждому объекту практики, полученному от сервера.
            data.schedules.forEach((schedule) => {
              // --- Создание чекбоксов, совместимых с Django ---
              // Чтобы корректно отправить данные для поля ManyToManyField с виджетом CheckboxSelectMultiple,
              // каждый <input type="checkbox"> должен иметь одинаковый атрибут 'name' (например, 'schedules')
              // и уникальный 'value' (ID услуги). При отправке формы браузер передаст
              // список всех выбранных ID услуг под ключом 'schedules'.

              // Создаем <div> для обертки чекбокса и его метки, чтобы соответствовать структуре Bootstrap.
              const div = document.createElement("div");
              div.className = "col-6 form-check";

              // Создаем сам элемент <input> для чекбокса.
              const input = document.createElement("input");
              input.type = "checkbox";
              // ВАЖНО: 'name' должен совпадать с именем поля в Django-форме ('schedules').
              input.name = "services";
              // 'value' будет первичным ключом (id) экземпляра модели Schedule.
              input.value = schedule.id;
              // Генерируем уникальный ID для самого input, чтобы связать его с <label>.
              input.id = `id_schedules_${schedule.id}`;
              input.className = "form-check-input";

              // Создаем <label> для чекбокса.
              const label = document.createElement("label");
              // Атрибут 'for' связывает метку с чекбоксом, улучшая доступность (клики по тексту метки).
              label.htmlFor = `id_schedules_${schedule.id}`;
              label.className = "form-check-label";
              label.textContent = schedule.date; // Отображаем дату практики.

              // Собираем конструкцию: добавляем <input> и <label> внутрь <div>.
              div.appendChild(input);
              div.appendChild(label);
              // Добавляем готовый элемент чекбокса в контейнер на странице.
              schedulesContainer.appendChild(div);
            });
          } else {
            // Если у инструктора нет практик, отображаем сообщение.
            schedulesContainer.innerHTML =
              '<p class="text-muted">У этого инструктора нет доступных практик.</p>';
          }
        })
        .catch((error) => {
          // Этот блок перехватывает ошибки из fetch-запроса (например, проблемы с сетью, ошибки сервера).
          console.error("Error fetching schedules:", error);
          // Отображаем сообщение об ошибке пользователю прямо в контейнере.
          schedulesContainer.innerHTML =
            '<p class="text-danger">Не удалось загрузить практики. Попробуйте позже.</p>';
        });
    });
  }
});