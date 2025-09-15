document.addEventListener("DOMContentLoaded", function () {
  // Находим выпадающий список расписаний и контейнер для отображения выбранной даты.
  const scheduleSelect = document.getElementById("id_schedule");
  const dateContainer = document.getElementById("id_schedule_date");

  // Добавляем обработчик события, который сработает каждый раз, когда пользователь меняет выбранное расписание.
  scheduleSelect.addEventListener("change", function () {
    // Получаем ID выбранного расписания. 'this.value' ссылается на атрибут 'value' выбранного <option>.
    const scheduleId = this.value;

    // Выполняем AJAX-запрос для получения выбранного расписания.
    fetch(`/get_schedule/${scheduleId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Обрабатываем полученные данные
        const scheduleDate = data.date;

        // Выводим тип данных в консоль
        console.log("AJAX-запрос выполнен");
        console.log("Type of scheduleDate:", typeof scheduleDate);

        // Обновляем контейнер с датой расписания
        dateContainer.textContent = scheduleDate;
      })
      .catch((error) => {
        console.error("Error loading schedule date:", error);
      });
  });
});