from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7181495252:AAGxTvEDSxYyI3eX24FL0Xdue3GW-5A_r7g'
BOT_USERNAME: Final = '@Pulcherskincare_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello! Thanks for chatting with me! <b>I am banana!</b>', 
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'I am a banana! <i>Please type something so I can respond!</i>', 
        parse_mode='HTML'
    )

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '<u>This is a custom command!</u>', 
        parse_mode='HTML'
    )

# Responses
def handle_response(text: str) -> str:
    if 'hello' in text:
        return '<b>Hey there</b>'
    
    if 'how are you' in text:
        return '<i>I am good</i>'
    
    if 'i love python' in text:
        return '<u>Remember to subscribe</u>'
    
    return '<code>I do not understand what you wrote...</code>'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling.....')
    app.run_polling(poll_interval=3)
