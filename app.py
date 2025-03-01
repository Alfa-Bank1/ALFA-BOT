from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    # Получаем user_id пользователя
    user_id = update.message.from_user.id

    # Формируем URL мини-апп с user_id
    web_app_url = f"https://alfa-bank-qul0g66u6-alfa-banks-projects.vercel.app?user_id={user_id}"

    # Создаем кнопку для открытия мини-апп
    keyboard = [
        [InlineKeyboardButton("Открыть мини-аппп", web_app={"url": web_app_url})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    await update.message.reply_text(
        "Нажмите кнопку, чтобы открыть мини-апп:",
        reply_markup=reply_markup
    )

# Основная функция
def main() -> None:
    # Вставьте сюда ваш токен
    application = Application.builder().token("7881963357:AAFa6Nf94JOYSDt-io0BshCgykIFIFJSVHs").build()

    # Регистрация обработчика команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()