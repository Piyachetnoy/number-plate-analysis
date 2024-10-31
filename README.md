・pipでインストールするライブラリ名をrequirements.txtに記載  
pip install -r requirements.txt でライブラリをまとめてインストール  

・注意
pythonのバージョンを最新(3.12.4)にすると動かなかった。pythonのバージョンを3.1にすると動いた。  
理由:pytorchなどのバージョンを古いものにする必要があったから
    python -m pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118
    以上のコードで旧バージョンのpytorchなどをインストールする必要がある
    最新バージョンのpython(3.12.4)ではpytorchのバージョンを一番古いもので2.2.0までしか下げることしかできないため，pytorchのバージョンを2.1.2にできないことが原因だと考えられる。


・使用したライブラリ  
Flask  
os  
byteslO  
pandas  
matplotlib  
japanize_matplotlib  
FigureCanvasAgg  
ultralytics  
easyocr  
cv2  
from PIL import Image,ImageDraw  
string  
torch==2.1.2  
torchvision==0.16.2  
torchaudio==2.1.2  
__________________________________

．ファイル配置  
/アプリ/  
|    
|-/results/  
|-/runs/detect/predict/  
|   |-/crops/number_plate/  
|-/templates/  
|   |-index.html  
|   |-/images/  
|   |-index_waka/html  
|-app.py  
|-best.pt  



