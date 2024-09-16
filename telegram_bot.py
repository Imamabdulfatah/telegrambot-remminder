import pyrebase
from telegram.ext import Updater, MessageHandler, Filters

firebaseConfig = {
    "apiKey": "AIzaSyCJkloB4abSy6v8CVmaETOfzLFdwBb2XZQ",
    "authDomain": "banjir-app.firebaseapp.com",
    "databaseURL": "https://banjir-app-default-rtdb.firebaseio.com",
    "projectId": "banjir-app",
    "storageBucket": "banjir-app.appspot.com",
    "messagingSenderId": "280622665477",
    "appId": "1:280622665477:web:31f12f031d27936d6b316c"
};

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Get users data from the database
users = db.child("users").get()
# sensors = db.child("Sensor").get()

# Convert users to a list of tuples (user_id, user_data)
users_list = list(users.val().items())
# sensor_list = list(sensors.val().items())[::-1]



# Function to print telegramId of a user at a specific index
def print_telegram_id(index):
    if index < len(users_list):
        user_id, user_data = users_list[index]
        telegram_id = user_data.get('telegramId')
        return telegram_id
    else:
        return None

def get_latest_jarak_air(location):
    # Fetch sensor data from the "Sensor" node for the specified location
    sensors = db.child("Sensor").order_by_child("lokasi").equal_to(location).limit_to_last(1).get()
    
    # Check if data exists for the specified location
    if sensors.each():
        for sensor in sensors.each():
            sensor_data = sensor.val()
            jarak_air = sensor_data.get('JarakAir')
            return jarak_air  # Return JarakAir value
    else:
        return None 
    
# Fungsi untuk menangani pesan yang masuk
def handle_message(update, context):


    # text = update.message.text.lower()  # Ambil pesan yang diterima dan ubah ke huruf kecil
    
    if get_latest_jarak_air(1) == 20:
        # chat_id = update.message.chat_id  # Ambil chatId dari pengirim pesan
        context.bot.send_message(chat_id=print_telegram_id(0), text='air akan banjir dilokasi 1 cepat')  
        context.bot.send_message(chat_id=print_telegram_id(1), text='air akan banjir dilokasi 2 lambat')  

def main():
    # Token bot yang diperoleh dari BotFather
    token = '6812610931:AAHw2AxbsOXzIBkIdaCzn41WMtqFDTu-PfI'
    
    # Buat Updater dan pass token bot Anda
    updater = Updater(token, use_context=True)
    
    # Ambil Dispatcher untuk mendaftarkan handler
    dp = updater.dispatcher
    
    # Tambahkan handler untuk pesan teks yang masuk
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Mulai bot
    updater.start_polling()
    
    # Biarkan bot berjalan sampai Ctrl+C ditekan
    updater.idle()

if __name__ == '__main__':
    main()
