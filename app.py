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
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')

            @after_this_request
            def remove_file(response):
                try:
                    os.remove(file_path)
                except Exception as error:
                    app.logger.error("Error removing or closing downloaded file", error)
                return response

            return send_file(file_path, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error during download: {e}")
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
