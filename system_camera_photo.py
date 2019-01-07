# -*- coding: utf-8 -*-

#このモジュールは画像処理に使われます．
#APIkeyが必要になります．google cloud vision からAPIkeyを各自取得してください    https://cloud.google.com/vision/?hl=ja
#

###########################################################
#各種関数の呼び出し##########################################
###########################################################
import re
import requests,base64,json#API関連の関数
import cv2


###########################################################
#実行関数の定義#############################################
###########################################################


#######################
#画像を読み込んで消費期限を表示する関数
#######################
class Img_process:
    def __init__(self,GOOGLE_CLOUD_VISION_API_URL,API_KEY):
        self.GOOGLE_CLOUD_VISION_API_URL=GOOGLE_CLOUD_VISION_API_URL
        self.API_KEY=API_KEY

    #画像読み込みとエンコード
    #IN  str　 ファイル場所
    #OUT bytes 画像
    #この関数で戻される画像はrequest_cloud_vison_apiに渡されます．
    def img_to_base64(self,filepath):
        with open(filepath, 'rb') as img:
            img_byte = img.read()
        return base64.b64encode(img_byte)
    
    
    #Google cloud visionの呼び出しと文字認識の実行
    #IN  bytes　 画像
    #OUT str 文字列読み取り結果
    #この関数で戻されるstrはexpiry_readに渡されます
    def cloud_vison_api(self,img):
        api_url = self.GOOGLE_CLOUD_VISION_API_URL + self.API_KEY
        req_body = json.dumps({#json列から必要な情報を取得
            'requests': [{
                'image': {
                    'content': img.decode('utf-8') # bytes2str
                },
                'features': [{
                    'type': 'TEXT_DETECTION', 
                    'maxResults': 5,
                }]
            }]
        })
        res = requests.post(api_url, data=req_body)
        full_text=res.json()
        text=full_text["responses"][0]["fullTextAnnotation"]["text"]
        return text
    
    
    #文字列から消費期限を抜き出します
    #IN  str  文字列読み取り結
    #OUT list(3) int  消費期限  ex)[18,2,13]　 2018年2月13日が消費期限の食品
    #この関数で戻されるstr
    #***この関数はヒューリスティックな処理を行っているため，改善の余地があります．***
    def expiry_read(self,text):
        text=re.sub(" ","",text)#半角削除
        text=re.sub("\n","",text)#改行削除
        text=re.findall(r'([0-9.]*)',text)#数字とdotを検索
        text=[i for i in text if i !=""]#""文字列を削除
        text=max(text,key=len)#一番長い文字列を抽出
        text=text.split(".") #dotを削除
        if len(text[0])==4:#年数を2桁に変更
            text[0]=text[0][2:]      
        text=[int(i) for i in text]
        return text


#######################
#webカメラを起動して画像を取得する関数
#######################
class Img_read:
    def video_capture(self,FILE_NAME):
        cap = cv2.VideoCapture(0)        
        while(True):
            ret, frame = cap.read()
            cv2.imshow('captured',frame)
            key = cv2.waitKey(1) & 0xFF        

            if key == ord('s'):
                cv2.imwrite(FILE_NAME,frame)
                break
        cap.release()
        cv2.destroyAllWindows()
