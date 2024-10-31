import os
import cv2
import csv
import datetime
import matplotlib.pyplot as plt
from ultralytics import YOLO
import easyocr
from PIL import Image, ImageDraw

def process_images(INPUT_PHOTO_PATH):
    # モデルのパス
    YAML_PATH = "C:/Users/rinra/Documents/data_analy/best.pt"

    class YoloNumberPlateCut:
        def __init__(self, yaml_path, input_photo_path):
            self.yaml_path = yaml_path
            self.input_photo_path = input_photo_path

        def yolo_cut(self):
            model = YOLO(self.yaml_path)
            results = model.predict(self.input_photo_path, save=True, save_crop=True, conf=0.1)
            # "runs"フォルダが自動生成され、predict->crops->number_plateに切り抜かれた画像が保存される
            # 生成された画像の名前は入力画像と同じになります

    class ReadNumber:
        def __init__(self, image_path):
            self.image_path = image_path

        def read(self):
            result_r = []
            reader = easyocr.Reader(['ja'])
            image = cv2.imread(self.image_path)
            bounds = reader.readtext(self.image_path)
            for idx in range(len(bounds)):
                res = bounds[idx][0]
                print(res)

            # 現在の解像度を確認
            height, width = image.shape[:2]
            print(f'元の解像度: {width} x {height}')

            # 解像度を300dpiに調整
            tmp = 500 / height
            new_height = int(height * tmp)  # 96dpiから300dpiへ
            new_width = int(width * tmp)
            resized_image = cv2.resize(image, (new_width, new_height))

            nimg = cv2.bitwise_not(resized_image)
            gimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2GRAY)
            ret2, bimg = cv2.threshold(gimg, 0, 255, cv2.THRESH_OTSU)
            dimg = cv2.bilateralFilter(bimg, 25, 75, 75)

            result2 = reader.readtext(gimg)

            # 結果をリストに追加
            if len(result2) > 3:
                result_r.append(result2[2][1])  # 数字
                #result_r.append(result2[0][1])  # 数字
                #result_r.append(result2[1][1])  # 数字
                #result_r.append(result2[3][1])  # 数字

            return result_r

    # インスタンスを作成しメソッドを呼び出す
    cut = YoloNumberPlateCut(YAML_PATH, INPUT_PHOTO_PATH)
    cut.yolo_cut()

    # 切り抜かれた画像のパス
    IMAGE_PATH = "C:/Users/rinra/Documents/data_analy/runs/detect/predict/crops/number_plate/test2.jpg"
    read_number = ReadNumber(IMAGE_PATH)
    result = read_number.read()
    print(result)

    # 現在の日付を取得
    today_date = datetime.date.today().strftime('%Y-%m-%d')

    # 結果をCSVファイルに保存する
    CSV_FILE_PATH = "C:/Users/rinra/Documents/data_analy/result.csv"
    with open(CSV_FILE_PATH, mode='w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["date", "region"])  # ヘッダー行
        for index, item in enumerate(result):
            writer.writerow([today_date, item])  # 日付と結果の各項目を新しい行として書き込む
