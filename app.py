# from flask import Flask, request, send_file, render_template, redirect, url_for
# import yt_dlp
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/download', methods=['POST'])
# def download():
#     url = request.form['url']
#     quality = request.form['quality']
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': quality,
#         }],
#         'outtmpl': 'downloads/%(title)s.%(ext)s',
#     }

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=True)
#             file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')
#         return send_file(file_path, as_attachment=True)
#     except Exception as e:
#         return redirect(url_for('index'))

# if __name__ == '__main__':
#     if not os.path.exists('downloads'):
#         os.makedirs('downloads')
#     app.run(host='0.0.0.0', debug=True)

from flask import Flask, request, send_file, render_template, redirect, url_for, after_this_request
import yt_dlp
import instaloader
import os
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form.get('quality', '192')
    if 'youtube.com' in url or 'youtu.be' in url:
        return download_youtube(url, quality)
    elif 'instagram.com' in url:
        return download_instagram(url)
    else:
        return redirect(url_for('index'))

def download_youtube(url, quality):
    # Detect whether ffmpeg is available for mp3 conversion
    ffmpeg_path = shutil.which('ffmpeg')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    # Only add the ffmpeg postprocessor if ffmpeg is installed
    if ffmpeg_path:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            prepared = ydl.prepare_filename(info_dict)

            # If conversion ran, the final file should be .mp3; otherwise keep original
            if ffmpeg_path:
                file_path = os.path.splitext(prepared)[0] + '.mp3'
            else:
                file_path = prepared

            # If file not found, try common audio/video extensions as fallback
            if not os.path.exists(file_path):
                base = os.path.splitext(prepared)[0]
                for ext in ('.webm', '.m4a', '.mp4', '.opus', '.mkv', '.flac', '.wav'):
                    candidate = base + ext
                    if os.path.exists(candidate):
                        file_path = candidate
                        break

            @after_this_request
            def remove_file(response):
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as error:
                    app.logger.error("Error removing or closing downloaded file: %s", error)
                return response

            if not os.path.exists(file_path):
                app.logger.error(f"Downloaded file not found: {file_path}")
                return redirect(url_for('index'))

            return send_file(file_path, as_attachment=True)
    except Exception as e:
        app.logger.error("Error during download: %s", e, exc_info=True)
        return redirect(url_for('index'))

def download_instagram(url):
    L = instaloader.Instaloader()
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])
        L.download_post(post, target='downloads')

        for file in os.listdir('downloads'):
            if file.endswith('.jpg') or file.endswith('.mp4'):
                file_path = os.path.join('downloads', file)

                @after_this_request
                def remove_file(response):
                    try:
                        os.remove(file_path)
                    except Exception as error:
                        app.logger.error("Error removing or closing downloaded file", error)
                    return response

                return send_file(file_path, as_attachment=True)

    except Exception as e:
        app.logger.error(f"Error during Instagram download: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(host='0.0.0.0', debug=True)
