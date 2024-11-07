# Project Setup Instructions

This guide provides instructions for setting up and installing necessary libraries for the project. Please follow each step carefully to avoid compatibility issues.

## Prerequisites

- **Python Version**: Ensure you are using **Python 3.10** for compatibility with the necessary versions of PyTorch libraries. Using the latest Python version (3.12.4) may cause compatibility issues as PyTorch version 2.1.2 and lower are not supported.

## Install Dependencies

1. **pip install libraries**

   ```bash
   pip install Flask,pandas,matplotlib,japanize_matplotlib,ultralytics,easyocr,torch==2.1.2,torchvision==0.16.2,torchaudio==2.1.2
   ```
   
## Project Dependencies

The following libraries are required for this project:

- Flask  
- os  
- bytesIO  
- pandas  
- matplotlib  
- japanize_matplotlib  
- FigureCanvasAgg  
- ultralytics  
- easyocr  
- cv2  
- Pillow (PIL) - `from PIL import Image, ImageDraw`  
- string  
- torch==2.1.2  
- torchvision==0.16.2  
- torchaudio==2.1.2  

<!-- 
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
--!>


