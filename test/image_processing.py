# image_processing.py
#flask検証用のファイル（実機能とは関係なし）
#このファイルで入力画像のサイズを取得しています
from PIL import Image

def process_image(image_path):
    """画像のサイズを取得する処理を行います"""
    img = Image.open(image_path)
    width, height = img.size
    return f"Width: {width}, Height: {height}"
