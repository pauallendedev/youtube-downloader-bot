from flask import Flask, request, render_template, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        quality = request.form['quality']
        return redirect(url_for('download', url=video_url, quality=quality))
    return render_template('index.html')

@app.route('/download')
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality')
    
    ydl_opts = {
        'format': quality,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(info_dict)
    
    return f"Descarga completada. Archivo guardado en: {file_path}"

if __name__ == '__main__':
    app.run(debug=True)
