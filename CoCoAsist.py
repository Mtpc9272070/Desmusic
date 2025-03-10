import telebot
import os
import socket
import re
from yt_dlp import YoutubeDL

# Configuración inicial 
TOKEN = '7638014907:AAHGV8FTMwRfzZwrcptp-nfSoKePsP-Hyj0'  # Reemplázalo con tu token real
bot = telebot.TeleBot(TOKEN)

# Configurar FFmpeg en el PATH
FFMPEG_PATH = "C:/ffmpeg/bin"
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# Aumentar el tiempo de espera para evitar "TimeoutError"
socket.setdefaulttimeout(300)  # 300 segundos (5 min)

# 📌 Función para limpiar el nombre de archivo
def clean_filename(text):
    """Limpia el título del video para que sea un nombre de archivo válido."""
    return re.sub(r'[^\w\s-]', '', text).replace(' ', '_')

# 📌 Función para descargar audio y generar URL
def download_audio(url):
    """Descarga el audio en MP3 y genera un link basado en el título."""
    output_path = 'descargas/%(title)s.%(ext)s'
    
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': output_path,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'retries': 3,  
        'noplaylist': True,  
        'quiet': False  
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = clean_filename(info.get('title', 'audio'))
            filename = f"{title}.mp3"
            filepath = f"descargas/{filename}"

            return filename, filepath
    except Exception as e:
        return None, f"Error: {e}"

# 📌 Mensaje de bienvenida automático
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Envía un mensaje de bienvenida."""
    bot.reply_to(message, "🎵 ¡Hola! Envíame el enlace de YouTube que deseas convertir en MP3.")

# 📌 Procesar URL y descargar audio
def process_url(message):
    """Procesa la URL y envía el link generado."""
    url = message.text

    if not url.startswith("http"):
        bot.reply_to(message, "❌ Ese no parece un enlace válido. Inténtalo de nuevo.")
        return
    
    bot.reply_to(message, "⏳ Procesando tu solicitud. Esto puede tardar unos segundos...")

    try:
        filename, filepath = download_audio(url)
        if filename is None:
            bot.reply_to(message, f"⚠️ Ocurrió un error: {filepath}")
        else:
            # Generar link basado en el título
            web_page = f"https://desmusic.render.com/audio/{filename.replace('.mp3', '')}"

            bot.reply_to(message, f"✅ Tu audio ha sido procesado con éxito. \n📥 Descárgalo aquí: \n🔗 {web_page}")

    except Exception as e:
        bot.reply_to(message, f"🚨 Hubo un error inesperado: {e}")

# 📌 Manejar mensajes con enlaces de YouTube
@bot.message_handler(func=lambda message: message.text.startswith("http"))
def handle_youtube_link(message):
    process_url(message)

# Iniciar el bot
bot.polling()
