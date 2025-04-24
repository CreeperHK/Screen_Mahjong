# Screen-Mahjong 螢幕截取麻將助手
利用YOLO模型進行手牌圖像辨識，其後使用演算法對目前手牌進行計算，判斷出目前最應該丟棄的手牌。

The YOLO model is used to recognize the hand tiles image, and then the algorithm is used to calculate the current hand tiles to determine the tile that should be discarded.

<b><h3>請注意，此工具目前僅適用於[雀魂](https://www.maj-soul.com/#/home)。
Please note that this tool is currently only available for [Maj-soul](https://www.maj-soul.com/#/home).</h3></b>

# Project-Dependencies 項目依賴
* Python 3.10+
* PIP
* Git (若可自行解壓縮可跳過 :: If you can decompress it yourself, you can skip this step.)

# How-To-Download 如何下載
1. 
    ```bash
    git clone https://github.com/CreeperHK/Screen_Mahjong
    ```
2. 
    ```bash
    cd Screen_Mahjong
    #(若需使用虛擬環境 請於此自行設置)
    #(If you need to use a virtual environment, please set it up here)
    ```

3. 
    ```bash
    pip install -r requirements.txt
    ```
4. 
    ```bash
    python capture.py
    ```

# How-To-Use 如何使用
將遊戲視窗調整為 1920x1080 並啟動工具，當你的手牌數量達到 14 張時，便會自動計算

Resize your game windows into 1920x1080 and start the program, When your hand tiles count reaches 14, it will be automatically calculated

# Special-Thanks 特別感謝
- skk294 for mahjongg: https://github.com/skk294/mahjongg
- Fat_X for Tile Checker: https://blog.csdn.net/qq_51273457/article/details/113100157
- Ultralytics YOLO for the lastest YOLO v11: https://docs.ultralytics.com/models/yolo11/
- CreeperHK for Ron Calculator: https://github.com/CreeperHK/ron-calculator