import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from flask import Flask, request, jsonify

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Flask
app = Flask(__name__)

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    web_app_url = f"https://alfa-bank-qul0g66u6-alfa-banks-projects.vercel.app?user_id={user_id}"

    keyboard = [
        [InlineKeyboardButton("Открыть мини-апп", web_app={"url": web_app_url})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Нажмите кнопку, чтобы открыть мини-апп:",
        reply_markup=reply_markup
    )

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    await update.message.reply_text(f"Вы написали: {text}")

# Инициализация бота
def setup_bot():
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("Токен бота не найден в переменных окружения!")
        return None

    application = Application.builder().token(token).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return application

# Обработчик вебхука
@app.route('/api/webhook', methods=['POST'])
def webhook():
    application = setup_bot()
    if not application:
        return jsonify({"status": "error", "message": "Бот не инициализирован"}), 500

    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return jsonify({"status": "ok"})

# Установка вебхука
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    token = os.getenv('BOT_TOKEN')
    if not token:
        return jsonify({"status": "error", "message": "Токен не найден"}), 500

    webhook_url = "https://https://alfa-bdz67fdvj-alfa-banks-projects.vercel.app//api/webhook"
    response = requests.get(f"https://api.telegram.org/bot{token}/setWebhook?url={webhook_url}")
    return jsonify(response.json())

# Запуск Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))