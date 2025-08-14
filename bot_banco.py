import os
import time
import telebot

# --- Token desde variable de entorno (Render) ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Falta la variable de entorno BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# --- Rutas seguras para carpeta 'archivos' ---
BASE_DIR = os.path.dirname(os.path.abspath(_file_))
ARCHIVOS_DIR = os.path.join(BASE_DIR, "archivos")
os.makedirs(ARCHIVOS_DIR, exist_ok=True)
MENSAJES_PATH = os.path.join(ARCHIVOS_DIR, "mensajes.txt")

@bot.message_handler(commands=['start', 'ping'])
def start_handler(message):
    bot.reply_to(message, "👋 Hola, envíame el token y lo guardo. Escribe /ping para probar.")

@bot.message_handler(content_types=['text'])
def recibir_token(message):
    txt = (message.text or "").strip()
    # Guarda el mensaje con timestamp y chat_id
    with open(MENSAJES_PATH, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {message.chat.id} | {txt}\n")
    bot.reply_to(message, "✅ Token recibido y guardado.")

def run():
    # Reintentos automáticos si el polling se cae
    while True:
        try:
            print("🤖 Iniciando polling…")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠ Error en polling: {e}. Reintentando en 5s…")
            time.sleep(5)

if _name_ == "_main_":
    run()