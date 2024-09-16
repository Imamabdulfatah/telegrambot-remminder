from typing import Final, Tuple, Optional
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os
from datetime import datetime

TOKEN: Final = '7181495252:AAGxTvEDSxYyI3eX24FL0Xdue3GW-5A_r7g'
BOT_USERNAME: Final = '@Pulcherskincare_bot'
REMINDER_CHAT_ID: Final = '1544942060'
REMINDER_CHAT_ID2: Final = '1544942077' 
REMINDER_CHAT_ID3: Final = ['1544942060', '434343443', '3434343434341']   # Ganti dengan ID chat atau ID grup Anda
PHOTO_DIR: Final = 'received_photos'  # Directory to store received photos
USER_DATA_FILE: Final = 'user_data.txt'  # File to store user data

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ensure the directory exists
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name

    # Save user details to the file
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f'{user_id},{user_name}\n')

    await update.message.reply_text(
        'Selamat datang di pulcher, Saya pulcherbot akan mengingatkan kamu agar lebih cantik', 
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Apa yang bisa saya bantu?', 
        parse_mode='HTML'
    )

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '<u>Ayo pakai sunscreen sekarang 😊 yuk bisa yuk</u><u> /help jika ingin minta tolong  </u><u> /schedule tunjukan hasil dari dokter  </u>', 
        parse_mode='HTML'
    )

def handle_response(text: str) -> Tuple[str, Optional[str]]:
    text = text.lower()
    if 'hello' in text:
        return '<b>Hey there</b>', None
    
    if 'i love python' in text:
        return '<u>Remember to subscribe</u>', None

    if 'mana foto' in text:
        return 'Ini fotonya:', 'path/image/custom/photo.png'  # Replace with the path to the photo you want to send
    
    return '<code>Saya tidak mengerti apa yang anda tanyakan!!</code>', None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response, photo_path = handle_response(new_text)
        else:
            return
    else:
        response, photo_path = handle_response(text)

    print('Bot:', response)

    if photo_path:
        with open(photo_path, 'rb') as photo:
            await update.message.reply_photo(photo=InputFile(photo), caption=response, parse_mode='HTML')
    else:
        await update.message.reply_text(response, parse_mode='HTML')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    
    chat_id = update.message.chat_id
    user_name = update.message.from_user.username or update.message.from_user.first_name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    caption = update.message.caption or 'no_caption'
    sanitized_caption = "".join(x for x in caption if x.isalnum() or x in "._- ")[:50]  # Sanitize caption and limit length
    
    file_name = f'{user_name}_{chat_id}_{timestamp}_{sanitized_caption}.jpg'
    file_path = os.path.join(PHOTO_DIR, file_name)
    
    await photo_file.download_to_drive(file_path)
    # await update.message.reply_text(f'Foto berhasil diterima dan disimpan di {file_path}')

async def send_reminder(bot, chat_id, message=None, photo_path=None):
    if message:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
    if photo_path:
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(chat_id=chat_id, photo=InputFile(photo), caption=message, parse_mode='HTML')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('schedule', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Errors
    app.add_error_handler(error)

    # Scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder, 'cron', hour=19, minute=49, args=[app.bot, REMINDER_CHAT_ID, '<b>Jangan lupa makan bakso di jam 20:20!</b>'])
    scheduler.add_job(send_reminder, 'cron', hour=15, minute=25, args=[app.bot, REMINDER_CHAT_ID2, '<b>Selamat bergabung!</b>'])
    scheduler.add_job(send_reminder, 'cron', hour=15, minute=26, args=[app.bot, REMINDER_CHAT_ID3, '<b>Sampai jumpa!</b>'])

    # Photo reminder
    photo_path = 'path/image/reminder/photo.jpeg'  # Replace with the path to the photo you want to send
    scheduler.add_job(send_reminder, 'cron', hour=16, minute=38, args=[app.bot, REMINDER_CHAT_ID, None, photo_path])
    
    scheduler.start()
    
    # Running the bot
    print('Polling.....')
    app.run_polling(poll_interval=3)
