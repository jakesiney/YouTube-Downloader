from flask import Flask, render_template, request, send_file, escape
from backend import download_video
from backend import get_available_stream_qualities
import io

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = escape(request.form['youtube_url'])
        success, stream_qualities, error_message = get_available_stream_qualities(
            youtube_url)
        if success:
            return render_template('index.html', youtube_url=youtube_url, stream_qualities=stream_qualities)
        else:
            return render_template('index.html', error_message=error_message)

    return render_template('index.html', youtube_url=None, stream_qualities=None)


@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form['youtube_url']
    selected_quality = request.form['selected_quality']
    success, video_bytes, error_message = download_video(
        youtube_url, selected_quality)
    if success:
        video_io = io.BytesIO(video_bytes)
        return send_file(video_io, as_attachment=True, download_name='video.mp4', mimetype='video/mp4')
    else:
        return render_template('index.html', error_message=error_message, youtube_url=youtube_url, stream_qualities=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
