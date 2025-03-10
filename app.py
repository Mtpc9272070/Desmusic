from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# 📌 Página de inicio
@app.route("/")
def home():
    return "<h1>Bienvenido a DesMusic 🎵</h1>"

# 📌 Página de descarga de audio con plantilla
@app.route("/audio/<audio_name>")
def audio_page(audio_name):
    audio_file = f"{audio_name}.mp3"
    audio_path = os.path.join("descargas", audio_file)

    if os.path.exists(audio_path):
        return render_template("audio_page.html", audio_name=audio_name, audio_url=f"/descargas/{audio_file}")
    else:
        return "<h2>❌ Archivo no encontrado.</h2>", 404

# 📌 Servir archivos MP3 en la carpeta de descargas
@app.route("/descargas/<filename>")
def download_file(filename):
    return send_from_directory("descargas", filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs("descargas", exist_ok=True)
    app.run(debug=True)
