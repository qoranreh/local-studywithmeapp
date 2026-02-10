from flask import Flask, render_template, send_from_directory, request, jsonify
import yt_dlp
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# 1. 메인 홈 화면 (이 부분이 빠져있었어요!)
@app.route('/')
def home():
    return render_template('index.html')

# 2. CSS 파일 경로 보정
@app.route('/index-C3yqPdoO.css')
def serve_css_fallback():
    return send_from_directory('static', 'index-C3yqPdoO.css')

# 3. 비디오 파일 직접 접근용
@app.route('/static/video.mp4')
def serve_video():
    return send_from_directory('static', 'video.mp4')

# 4. 다운로드 로직
@app.route('/download', methods=['POST'])
def download():
    # 리액트 UI에 따라 request.form['url'] 대신 JSON을 받을 수도 있으므로 안전하게 처리
    url = request.form.get('url') or request.json.get('url')
    
    if not url:
        return "URL이 없습니다!", 400

    # yt-dlp 옵션 (static 폴더에 video.mp4로 저장)
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'static/video.mp4',
        'overwrites': True,
    } 
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "success" # 리액트 UI가 'success'를 기다릴 수 있음
    except Exception as e:
        return str(e), 500
g
if __name__ == '__main__':
    app.run(debug=True)