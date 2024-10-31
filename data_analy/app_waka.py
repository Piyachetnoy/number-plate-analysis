from flask import Flask, render_template, request, redirect, url_for, jsonify,make_response,session
import os
from io import BytesIO
import pandas as pd
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import japanize_matplotlib

from kaiseki_new import process_images

# Matplotlibのバックエンドを設定
matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = os.urandom(24) # セッションのためのシークレットキー

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
    result = process_images(file_path)

    return jsonify({'result': 'アップロード完了しました'})

@app.route('/submit_date', methods=['POST'])
def submit_date():
    date_start = request.form.get('date_start')
    date_finish = request.form.get('date_finish')

    # 日付が指定されていない場合のチェック
    if not date_start or not date_finish:
        return jsonify({'result': '開始日または終了日が指定されていません'}), 400
    
    # セッションに日付を保存
    session['date_start'] = date_start
    session['date_finish'] = date_finish
    
    # 日付を処理する処理
    result = process_dates(date_start,date_finish)
    return jsonify({'result': result})

def process_dates(date_start_str, date_finish_str):
    # 日付を処理する例
    return f"選択された開始日: {date_start_str}, 終了日: {date_finish_str}"

@app.route('/submit_choice', methods=['GET','POST'])
def submit_choice():
    # フォームデータから選択肢の値を取得
    selected_option = request.form.get('option')

    # セッションから日付を取得
    date_start = session.get('date_start')
    date_finish = session.get('date_finish')

    # 日付が指定されていない場合のチェック
    if not date_start or not date_finish:
        return jsonify({'result': '開始日または終了日が指定されていません'}), 400

    # ファイルの存在確認
    file1_path = 'result.csv'
    file2_path = 'GroupB_analy_data2.csv'

    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        return jsonify({'result': 'CSVファイルが見つかりません'}), 400

    df = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    #日付をdatetime型に変換 ⇐ 参考文献真似したけど、なんでこれをするのか謎
    df['date'] = pd.to_datetime(df['date'])
    date_start = pd.to_datetime(date_start)
    date_finish = pd.to_datetime(date_finish)

    #日付でデータをフィルタリング
    df = df[(df['date'] >= date_start) & (df['date'] <= date_finish)]

    if (selected_option == "地域別"):
        response = region_data(df)
    
    elif (selected_option == "県別"):
        response = prefecture_data(df,df2)

    else:
        return jsonify({'result': '選択されてないです'}), 400
    
    return response

def region_data(df):
    region_counts = df['region'].value_counts()
    sorted_regions = pd.DataFrame({'region':region_counts.index,'count':region_counts.values})
        
    #棒グラフ
    fig, ax = plt.subplots()
    ax.bar(sorted_regions['region'], sorted_regions['count'])
    ax.set_xlabel('地域')
    ax.set_ylabel('回数')
    ax.grid(axis = 'y')
    ax.set_title('地域別統計')

    #canvasに画像を出力
    canvas = FigureCanvasAgg(fig)

    #Bytesを使用して仮想的にメモリ上に書き出す
    png_output = BytesIO()
    canvas.print_png(png_output)

    #画像データをレスポンスで作成
    data = png_output.getvalue()
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)

    #jpegに変換！かも
    #image = os.path.join(app.config['RESULT_FOLDER'], 'graph_region.jpg')
    #plt.savefig(image, format='jpeg')
    #plt.close()

    return response

def prefecture_data(df,df2):
    #都道府県割り当て
    df3 = pd.merge(df, df2, on='region')

    #都道府県をカウントする関数
    prefecture_counts = df3['prefecture'].value_counts()
    sorted_prefectures = pd.DataFrame({'prefecture':prefecture_counts.index,'count':prefecture_counts.values})

    #棒グラフ
    fig, ax = plt.subplots()
    ax.bar(sorted_prefectures['prefecture'], sorted_prefectures['count'])
    ax.set_xlabel('都道府県')
    ax.set_ylabel('回数')
    ax.grid(axis = 'y')
    ax.set_title('都道府県別統計')

    #jpegに変換！かも
    #img_data = os.path.join(app.config['RESULT_FOLDER'], 'graph_prefecture.jpg')
    #plt.savefig(img_data, format='jpeg')
    #plt.close()

    #canvasに画像を出力
    canvas = FigureCanvasAgg(fig)

    #Bytesを使用して仮想的にメモリ上に書き出す
    png_output = BytesIO()
    canvas.print_png(png_output)

    #画像データをレスポンスで作成
    data = png_output.getvalue()
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)

    return response

if __name__ == '__main__':
    app.run(debug=True)