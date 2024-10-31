# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from image_processing import process_image  # 上記のPythonコードをインポート

app = Flask(__name__)

# アップロードされた画像を保存するディレクトリ
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'result': 'No image uploaded'}), 400

    image = request.files['image']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    
    # 画像をローカルに保存
    image.save(file_path)
    
    # （検証用の仮の機能）画像を処理
    result = process_image(file_path)

    return jsonify({'result': result})

@app.route('/submit_date', methods=['POST'])
def submit_date():
    selected_date = request.form.get('date')
    
    # 日付を処理する処理
    result = process_date(selected_date)

    return jsonify({'result': result})

def process_date(date_str):
    # 日付を処理する例
    return f"選択された日付は: {date_str}"


@app.route('/submit_choice', methods=['POST'])
def submit_choice():
    # フォームデータから選択肢の値を取得
    selected_option = request.form.get('option')
    
    if selected_option:
        # 受け取った選択肢の文字列で何らかの処理を行う
        result = process_choice(selected_option)
        return jsonify({'result': result})
    else:
        return jsonify({'result': 'No option selected'}), 400

def process_choice(choice):
    # 選択肢に基づいて処理を行う（例: 選択肢の文字列を返す）
    return f"選択されたオプションは: {choice}"


if __name__ == '__main__':
    app.run(debug=True)
