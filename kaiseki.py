import os
import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2
import easyocr
from PIL import Image, ImageDraw

#best.yamlを指していますが、ここはアプリ化の時にbest.yamlの位置は変わると思うので変更してください。
YAML_PATH = "C:/Users/rinra/Documents/data_analy/best.pt"

#入力画像を代入してください。pathをグローバル変数に代入していますが、適宜変更してください。
INPUT_PHOTO_PATH = "C:/Users/rinra/Documents/data_analy/templates/images/test2.jpg"

class YoloNumberPlateCut:
    def __init__(self):
        pass

    @staticmethod
    def yolo_cut():
        yaml_path = YAML_PATH
        input_photo_path = INPUT_PHOTO_PATH
        model = YOLO(yaml_path)
        results = model.predict(input_photo_path,save=True, save_crop=True, conf=0.1)
        #runsフォルダが自動生成され、predict->crops->number_plateに切り抜かれた画像がアップロードされる
        #生成された画像の名前は入力された画像の名前と同じになります

#切り抜かれた画像のパス
IMAGE_PATH = "C:/Users/rinra/Documents/data_analy/runs/detect/predict/crops/number_plate/test2.jpg"

class ReadNumber:
    def __init__(self):
        pass

    @staticmethod
    def read():
        img_path = IMAGE_PATH
        reader = easyocr.Reader(['ja'])
        image = cv2.imread(img_path)

        # 現在の解像度を確認
        height, width = image.shape[:2]
        print(f'元の解像度: {width} x {height}')

        # 解像度を600dpiに調整
        tmp = 500 / height
        new_height = int(height * tmp)
        new_width = int(width * tmp)
        resized_image = cv2.resize(image, (new_width, new_height))

        result = reader.readtext(resized_image)
        print(result)

        fresult = []
        for i in result:
            rect, v, a = i
            (x1, y1) = rect[0]
            (x2, y2) = rect[2]
            print(x1, y1, x2, y2)
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            print(x1, y1, x2, y2)
            
            reimage = resized_image[y1:y2, x1:x2]

            nimg = cv2.bitwise_not(reimage)
            gimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2GRAY)
            result2 = reader.readtext(gimg, detail=0)

            if((any(c.isdigit() for c in result2[0]))==True):
              ans=result2[0].split(' ')
              for j in ans:
                fresult.append(j)
            if(len(result[0])==1):
              fresult.append(result2[0])
        return fresult

# クラスメソッドの呼び出し
cut = YoloNumberPlateCut()
cut.yolo_cut()

read_number = ReadNumber()
result = read_number.read()
print(result)
