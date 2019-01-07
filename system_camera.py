# -*- coding: utf-8 -*-

import os
import system_camera_photo as photo

import numpy as np
#_________________________________________________________#
#定数の定義________________________________________________#
#_________________________________________________________#
GOOGLE_CLOUD_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate?key="#クエリ送信先
os.chdir("F:\講義\システム制御プロジェクト")#APIkeyの場所
API_KEY = str(np.loadtxt("APIkey.txt",dtype="str")) #APIキー
FILE_DIR="F:\講義\システム制御プロジェクト\img"#画像ファイルの場所
OUTPUT_IMG="1.jpg"#画像の名前

#######################
#関数の実行#############
#######################

#ファイル場所の変更
os.chdir(FILE_DIR)


#インスタンス化
img_read=photo.Img_read()
img_process=photo.Img_process(GOOGLE_CLOUD_VISION_API_URL,API_KEY)

#webカメラを起動して画像取得
#img_read.video_capture(OUTPUT_IMG)

#画像を処理
img_to_base64_output =img_process.img_to_base64(OUTPUT_IMG)
cloud_vison_api_output = img_process.cloud_vison_api(img_to_base64_output)
expiry_read_output=img_process.expiry_read(cloud_vison_api_output)

print(expiry_read_output)




