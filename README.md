# Volunteer Data Collection Bot

## Описание проекта
Telegram-бот для сбора данных о волонтёрах IT, участвующих в экологических мероприятиях, связанных с ликвидацией последствий разлива нефтепродуктов. Бот сохраняет данные пользователей в базу данных SQLite, поддерживает обработку шагов заполнения формы и учитывает ограничение в три никнейма на одного пользователя.

---

## Основной функционал
1. **Регистрация пользователя**:
   - Никнейм (обязательно).
   - Компетенции (обязательно).
   - Роли (обязательно).
   - Часовой пояс (необязательно, можно пропустить).
   - Предпочтительное время (необязательно, можно пропустить).
   - GitHub (необязательно, можно пропустить).
   - Дополнительные данные (необязательно, можно пропустить).
2. **Сохранение данных** в базу SQLite с учётом ограничений (не более 3 никнеймов на одного пользователя).
3. **Обработка исключений и пограничных случаев** (например, попытка регистрации с превышением лимита никнеймов).

---

## Установка и запуск

### Требования
- Python 3.10+
- Установленные зависимости из `requirements.txt`

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone git@gitlab.com:rus4787/volunteer_data_bot.git
   cd volunteer_data_bot
   ```
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate   # Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте файл `secrets.toml` для хранения токена бота:
   ```toml
   secret_token = { TOKEN_tell = "<ваш токен>" }
   ```
5. Запустите бота:
   ```bash
   python main.py
   ```

---

## Структура проекта

### Основные файлы
- **`main.py`**: Главный файл для запуска бота. Содержит обработчики команд и шагов регистрации.
- **`database.py`**: Логика работы с базой данных SQLite (создание таблиц, добавление пользователей, обработка ограничений).
- **`requirements.txt`**: Список зависимостей проекта.
- **`secrets.toml`**: Файл для хранения конфиденциальной информации (токен бота).

### Таблица базы данных
- **users**:
  - `id` (INTEGER): Уникальный идентификатор записи.
  - `user_id` (INTEGER): Telegram ID пользователя.
  - `nickname` (TEXT): Никнейм в Telegram (обязательное поле).
  - `competencies` (TEXT): Компетенции пользователя (обязательное поле).
  - `roles` (TEXT): Роли пользователя (обязательное поле).
  - `tracker_access` (BOOLEAN): Доступ к трекеру.
  - `timezone` (INTEGER): Часовой пояс (может быть `NULL`).
  - `preferred_time` (TEXT): Предпочтительное время (может быть `NULL`).
  - `github` (TEXT): Ссылка на GitHub (может быть `NULL`).
  - `additional_data` (TEXT): Дополнительные данные (может быть `NULL`).
  - `form_status` (TEXT): Статус заполнения формы.
  - `created_at` (TIMESTAMP): Время создания записи.

---

## Сценарии работы

### Последовательность шагов регистрации
1. Пользователь нажимает "Регистрация".
2. Заполняет никнейм. Если поле пустое, выводится ошибка и повторный запрос.
3. Заполняет компетенции. Аналогичная проверка обязательности.
4. Указывает роль. Проверка обязательности.
5. Часовой пояс — необязательное поле. Пустое сообщение пропускает шаг.
6. Предпочтительное время — необязательное поле. Пустое сообщение пропускает шаг.
7. GitHub — необязательное поле. Пустое сообщение пропускает шаг.
8. Дополнительные данные — необязательное поле. Пустое сообщение пропускает шаг.
9. После завершения регистрация подтверждается и данные сохраняются в базу.

### Пограничные случаи
1. **Превышение лимита никнеймов:** Если пользователь пытается зарегистрировать более 3 никнеймов, выводится сообщение об ошибке: "Пользователь с user_id <ID> уже имеет 3 никнейма."
2. **Пропуск необязательных полей:** Пустое сообщение для необязательных полей пропускает шаг.
3. **Повторная регистрация:** При повторном входе бот начинает с запроса ника и загружает текущие данные пользователя, если он уже зарегистрирован.

---

## Дополнения для разработчиков

### Логика обработки шагов
Каждый шаг регистрации связан с состоянием пользователя (`context.user_data['state']`). Основные обработчики:
- `handle_nickname`: Ввод никнейма.
- `handle_competencies`: Ввод компетенций.
- `handle_roles`: Указание ролей.
- `handle_timezone`: Указание часового пояса.
- `handle_preferred_time`: Указание предпочтительного времени.
- `handle_github`: Ввод GitHub.
- `handle_additional_data`: Дополнительные данные и сохранение.

### Расширение функционала
- Для добавления новых шагов регистрации добавьте состояние и соответствующий обработчик.
- Для изменения структуры базы данных используйте метод транзакций в `database.py`.

### Обработка ошибок
Все исключения логируются в терминале и, при необходимости, возвращаются пользователю. Обработчик ошибок:
```python
async def error_handler(update: object, context: CallbackContext) -> None:
    print(f"Произошла ошибка: {context.error}")
```

---

## Контакты разработчиков
- Telegram: @rus4787
- GitLab: [Проект на GitLab](https://gitlab.com/rus4787/volunteer_data_bot)

---


