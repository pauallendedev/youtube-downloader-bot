from flask import Flask, request, render_template, send_file, jsonify
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formats', methods=['POST'])
def get_formats():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            filtered = [
                {
                    'format_id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('resolution') or f.get('height', 'audio'),
                    'note': f.get('format_note', '')
                }
                for f in formats if f.get('vcodec') != 'none' or f.get('acodec') != 'none'
            ]
            return jsonify({'formats': filtered})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_id = request.form['format']

    try:
        tmp_dir = tempfile.gettempdir()
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
