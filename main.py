import requests
import time
import warnings
warnings.filterwarnings("ignore", message="python-telegram-bot is using upstream urllib3")
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Ganti dengan token bot Anda
TELEGRAM_BOT_TOKEN = ''

# Penyimpanan token untuk setiap pengguna
user_tokens = {}
# Penyimpanan waktu notifikasi terakhir untuk setiap pengguna
last_notification_time = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome!\nUse /set "your_auth_token" to get notif Grass.\nBingung Liat Tutor:\nhttps://t.me/kelasmalamairdrop/82')

def set_token(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if context.args:
        token = context.args[0].strip('"')  # Menghapus tanda kutip
        user_tokens[user_id] = token
        last_notification_time[user_id] = 0  # Inisialisasi waktu notifikasi terakhir

        # Kirim notifikasi segera setelah token diset
        check_account_info(token, user_id)
        
        update.message.reply_text('Token Berhasil Tersimpan,\nKamu Akan Menerima Notif Setiap 1 Jam Sekali.')
    else:
        update.message.reply_text('Harap sertakan token setelah perintah /set.')

def send_message_to_telegram(message, user_id):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': user_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f'Error sending message to user {user_id}: {e}')

def get_auth_tokens():
    return user_tokens  # Menggunakan dict yang menyimpan token per user

URL = 'https://api.getgrass.io/epochEarnings?input=%7B%22isLatestOnly%22:false%7D'

def retrieve_username(auth_token):
    url = 'https://api.getgrass.io/retrieveUser'
    headers = {
        'Authorization': auth_token  # Tidak menggunakan "Bearer"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Cek jika terjadi error pada response
        data = response.json()
        
        # Ambil username dari respons
        username = data['result']['data']['username']  # Akses username dengan benar
        return username
    except requests.exceptions.RequestException as e:
        print(f'Error retrieving username: {e}')
        return None
    except KeyError as e:
        print(f'KeyError: {e} - Data respons mungkin tidak terstruktur dengan benar atau kehilangan kunci yang diharapkan.')
        return None

def check_account_info(auth_token, user_id):
    headers = {
        'Authorization': auth_token  # Tidak menggunakan "Bearer"
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Cek jika terjadi error pada response
        data = response.json()
        
        # Ambil informasi yang diinginkan
        account_data = data['result']['data']['data'][0]
        stage = account_data['stage']
        total_points = account_data['totalPoints']
        total_uptime = account_data['totalUptime']
        epoch_name = account_data['epochName']

        # Ambil username
        username = retrieve_username(auth_token)

        # Format modified untuk menampilkan tahun-bulan-hari
        modified = datetime.strptime(account_data['modified'], "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date = modified.strftime("%Y-%m-%d")

        # Format pesan
        message = (
            f"━━━🌿GRASS NOTIF🌿━━━\n\n"
            f"🔔 *Info Akun*: {username}\n"  
            f"〽️ *Stage*: {stage}\n"
            f"💸 *Total Point*: {total_points}\n"
            f"💰 *Total Uptime*: {total_uptime}\n"
            f"♻️ *Epoch Name*: {epoch_name}\n"
            f"⏰ *Modified*: {formatted_date}\n\n"
            f"_Notif Di Kirim Setiap 1 Jam Sekali_\n"
            f"*Follow Channel Biar Ga Mati Nih Bot*\n"
            f"━━━@airdroptodayreal━━━" # DONT REMOVE THIS CHANNELTAG
        )

        # Kirim pesan ke Telegram jika waktunya sudah tepat
        current_time = time.time()
        if current_time - last_notification_time[user_id] >= 3600:  # 3600 detik = 1 jam
            send_message_to_telegram(message, user_id)
            last_notification_time[user_id] = current_time  # Update waktu notifikasi terakhir

    except requests.exceptions.RequestException as e:
        print(f'Error for Account {user_id}: {e}')
    except (KeyError, IndexError) as e:
        print(f'Error in data structure for Account {user_id}: {e}')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Menambahkan handler untuk perintah
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set", set_token))

    updater.start_polling()

    # Jalankan fungsi setiap 2 menit untuk masing-masing akun
    while True:
        for user_id, auth_token in user_tokens.items():
            check_account_info(auth_token, user_id)
        time.sleep(3600)  # Tunggu selama 2 menit (120 detik) sebelum memeriksa lagi

if __name__ == '__main__':
    main()
