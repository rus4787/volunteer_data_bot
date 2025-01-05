import tomli
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
from database import add_user
from telegram.error import TelegramError

async def error_handler(update: object, context: CallbackContext) -> None:
    print(f"Произошла ошибка: {context.error}")

# Чтение токена из файла secrets.toml
def load_token():
    with open("secrets.toml", "rb") as f:
        secrets = tomli.load(f)
    return secrets["secret_token"]["TOKEN_tell"]

# Токен для бота
TOKEN = load_token()

# Стартовая команда
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_photo(
        photo=open("DALLE.png", "rb"),  # Убедитесь, что файл DALLE.png находится в той же папке
        caption=(
            f"Привет, {user.first_name}! \n\n"
            "Добро пожаловать в бота волонтеров IT! 🌊 Мы боремся с последствиями разлива нефтепродуктов в Черном море у берегов Анапы. "
            "Наша миссия — спасение морской флоры и фауны, очистка побережья от мазута и поддержка экологической команды. "
            "Каждый волонтер важен!🛟 Спасибо за вашу помощь природе! 🌿\n\n"
            "Если вы хотите зарегистрироваться, нажмите кнопку ниже.💻"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Регистрация", callback_data="register")],
            [InlineKeyboardButton("Отмена", callback_data="cancel")]
        ])
    )

# Обработчик для кнопки "Регистрация"
async def register_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    print(f"Кнопка 'Регистрация' нажата пользователем {query.from_user.id}")
    await query.answer()

    # Скрываем кнопки, оставляя текст
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception as e:
        print(f"Ошибка при скрытии кнопок: {e}")

    # Отправляем новое сообщение
    await query.message.reply_text("Давайте начнем! Введите ваш ник в Telegram:")
    context.user_data['state'] = 'enter_nickname'


# Обработчик для кнопки "Отмена"
async def cancel_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    print(f"Кнопка 'Отмена' нажата пользователем {query.from_user.id}")
    await query.answer()

    # Скрываем кнопки, оставляя текст
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception as e:
        print(f"Ошибка при скрытии кнопок: {e}")

    # Отправляем новое сообщение
    await query.message.reply_text("Регистрация отменена. Если вы передумаете, нажмите /start.")


# Обработчик ввода ника
async def handle_nickname(update: Update, context: CallbackContext):
    if context.user_data.get('state') == 'enter_nickname':
        user_id = update.effective_user.id
        nickname = update.message.text.strip()  # Убираем лишние пробелы

        if not nickname:  # Проверка обязательного поля
            await update.message.reply_text("Никнейм обязателен. Пожалуйста, введите ваш никнейм:")
            return

        context.user_data['nickname'] = nickname  # Сохраняем никнейм во временное хранилище

        # Переход на следующий этап
        context.user_data['state'] = 'enter_competencies'
        await update.message.reply_text("Ваш ник успешно зарегистрирован! Теперь введите ваши компетенции:")
    else:
        await update.message.reply_text("Нажмите /start, чтобы начать.")



async def handle_competencies(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    if not text:  # Проверка на пустое сообщение
        await update.message.reply_text("Компетенции обязательны. Пожалуйста, укажите ваши компетенции:")
        return

    context.user_data['competencies'] = text
    context.user_data['state'] = 'enter_roles'
    await update.message.reply_text("Выберите вашу роль из списка (например, Frontend, Backend, Дизайн):")


async def handle_roles(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    if not text:  # Проверка на пустое сообщение
        await update.message.reply_text("Роль обязательна. Пожалуйста, укажите вашу роль:")
        return

    context.user_data['roles'] = text
    context.user_data['state'] = 'enter_timezone'
    await update.message.reply_text(
        "Укажите ваш часовой пояс (например, +3). Если хотите пропустить, отправьте пустое сообщение:"
    )


async def handle_timezone(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    context.user_data['timezone'] = text if text else None
    context.user_data['state'] = 'enter_preferred_time'
    await update.message.reply_text(
        "Укажите предпочтительное время (например, ПН-ПТ, 4 часа, 10:00-18:00). "
        "Если хотите пропустить, отправьте пустое сообщение:"
    )


async def handle_preferred_time(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    context.user_data['preferred_time'] = text if text else None
    context.user_data['state'] = 'enter_github'
    await update.message.reply_text(
        "Введите ваш GitHub (или отправьте пустое сообщение, чтобы пропустить):"
    )


async def handle_github(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    context.user_data['github'] = text if text else None
    context.user_data['state'] = 'enter_additional_data'
    await update.message.reply_text(
        "Введите дополнительные данные (или отправьте пустое сообщение, чтобы пропустить):"
    )


async def handle_additional_data(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    context.user_data['additional_data'] = text if text else None

    # Сохранение данных в базу
    try:
        add_user(
            user_id=update.effective_user.id,
            nickname=context.user_data['nickname'],
            competencies=context.user_data['competencies'],
            roles=context.user_data['roles'],
            tracker_access=True,  # Предполагаем, что доступ к трекеру есть
            timezone=context.user_data.get('timezone'),
            preferred_time=context.user_data.get('preferred_time'),
            github=context.user_data.get('github'),
            additional_data=context.user_data.get('additional_data'),
            form_status='заполнено'
        )
        await update.message.reply_text("Регистрация завершена. Спасибо!")
    except ValueError as e:  # Обработка ошибки с никнеймами
        await update.message.reply_text(str(e))
        
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при сохранении данных: {e}")

    # Очистка состояния
    context.user_data.clear()


# Обработчик для ввода данных
async def handle_user_input(update: Update, context: CallbackContext):
    state = context.user_data.get('state')
    
    if not state:  # Если состояния нет
        await update.message.reply_text("Вы не начали процесс регистрации. Нажмите /start, чтобы начать.")
        return
    
    text = update.message.text.strip()

    if state == 'enter_nickname':
        await handle_nickname(update, context)
    elif state == 'enter_competencies':
        await handle_competencies(update, context)
    elif state == 'enter_roles':
        await handle_roles(update, context)
    elif state == 'enter_timezone':
        await handle_timezone(update, context)
    elif state == 'enter_preferred_time':
        await handle_preferred_time(update, context)
    elif state == 'enter_github':
        await handle_github(update, context)
    elif state == 'enter_additional_data':
        await handle_additional_data(update, context)

        
# Создаём бота
def main():
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(register_callback, pattern="^register$"))
    app.add_handler(CallbackQueryHandler(cancel_callback, pattern="^cancel$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))
    app.add_error_handler(error_handler)

    # Запускаем бота
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()


