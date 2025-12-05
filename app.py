from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # Allows your Netlify site to talk to this server

@app.route('/')
def home():
    return "Galactic Backend is Active"

@app.route('/get-video', methods=['GET'])
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Options to get the direct video link without downloading files to the server
        ydl_opts = {
            'format': 'best',  # Best quality
            'quiet': True,
            'no_warnings': True,
            'geo_bypass': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info
            info = ydl.extract_info(url, download=False)
            
            # Get the best url
            video_url = info.get('url', None)
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail', '')
            
            return jsonify({
                'status': 'success',
                'title': title,
                'thumbnail': thumbnail,
                'download_url': video_url
            })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)