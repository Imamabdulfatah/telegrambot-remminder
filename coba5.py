from typing import Final, Tuple, Optional
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os

TOKEN: Final = '7181495252:AAGxTvEDSxYyI3eX24FL0Xdue3GW-5A_r7g'
BOT_USERNAME: Final = '@Pulcherskincare_bot'
REMINDER_CHAT_ID: Final = '1544942060'  # Ganti dengan ID chat atau ID grup Anda
PHOTO_DIR: Final = 'received_photos'  # Directory to store received photos

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Pastikan direktori ada
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Selamat datang di pulcher, Saya pulcherbot akan mengingatkan kamu agar lebih cantik', 
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'apa yang bisa saya bantu', 
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
        return 'Ini fotonya:', 'path/image/custom/photo.png'  # Ganti dengan path ke foto yang ingin dikirim
    
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
    file_path = os.path.join(PHOTO_DIR, f'{photo_file.file_id}.jpg')
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

    # Perintah
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('schedule', custom_command))

    # Pesan
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Kesalahan
    app.add_error_handler(error)

    # Penjadwal
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder, 'cron', hour=19, minute=49, args=[app.bot, REMINDER_CHAT_ID, '<b>Jangan lupa makan bakso di jam 20:20!</b>'])
    scheduler.add_job(send_reminder, 'cron', hour=15, minute=25, args=[app.bot, REMINDER_CHAT_ID, '<b>Selamat bergabung!</b>'])
    scheduler.add_job(send_reminder, 'cron', hour=15, minute=26, args=[app.bot, REMINDER_CHAT_ID, '<b>Sampai jumpa!</b>'])

    # Penjadwal foto
    photo_path = 'path/image/reminder/photo.jpeg'  # Ganti dengan path ke foto yang ingin dikirim
    scheduler.add_job(send_reminder, 'cron', hour=16, minute=38, args=[app.bot, REMINDER_CHAT_ID, None, photo_path])
    
    scheduler.start()
    
    # Menjalankan bot
    print('Polling.....')
    app.run_polling(poll_interval=3)
