#==============================================================================================================
#未決定
#・データの取り扱い(DBを使うorファイルで管理orデモのみを想定して初めからコードに書いておく)
#・線引き用の画像どこから入手するのかどこに置くのか
#・そもそも1/4区切りとかなら残量入力をチェックボックスとかでやっても労力対して変わらない説
#未実装
#Main Page:期限によるリストの色付け
#Name Input Page:その他の商品認識方法
#Date Input Page:その他の賞味期限認識方法
#Edit Page:線引きによる残量入力
#Edit Page:線引きによる残量入力が正しいか確認するポップアップ？

#色々冗長な所があるのは許して
#==============================================================================================================

#==============================================================================================================
#ライブラリ
#==============================================================================================================
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkm
import random
from tkinter import StringVar
import datetime
import tkinter.messagebox as tkmsg
import functools

#==============================================================================================================
#関数定義
#==============================================================================================================

#---------------------------------------- Main Page -------------------------------------------------------
#名称ソートボタンが押された時に呼ばれる関数
def name_sort(stock, var, sort_btn1, sort_btn2):
    stock.sort(key = lambda x: x[0])
    name_list = []
    for i in range(len(stock)):
        name_list.append(stock[i][0] + "    日付:" + str(stock[i][1]) + "   残量:" + str(stock[i][2]) + "%")
    var.set(name_list)
    sort_btn1.state(["pressed"])
    sort_btn2.state(["!pressed"])

#期限ソートボタンが押された時に呼ばれる関数
def deadline_sort(stock, var, sort_btn1, sort_btn2):
    stock.sort(key = lambda x: x[1])
    name_list = []
    for i in range(len(stock)):
        name_list.append(stock[i][0] + "    日付:" + str(stock[i][1]) + "   残量:" + str(stock[i][2]) + "%")
    var.set(name_list)
    sort_btn1.state(["!pressed"])
    sort_btn2.state(["pressed"])

#Main Pageでリストボックス選択時のイベント
def listbox_selected(event, index, edit_page, item_label_text):
    if len(event.widget.curselection()) == 0:
        return
    index.set(event.widget.curselection()[0])
    index = int(index.get())
    label = event.widget.get(index)
    edit_page.tkraise()
    item_label_text.set(label)

#Main Pageでリストの期限による色付け
def coloring_list(stock,listbox):
    now = datetime.date.today()
    for i in range(len(stock)):
        delta = stock[i][1] - now
        #print(delta)
        if delta < datetime.timedelta(days=0): #期限切れ
            listbox.itemconfig(i, {'bg': 'red'})
        elif delta <= datetime.timedelta(days=3): #三日前
            listbox.itemconfig(i,{'bg': 'yellow'})
        else:
            listbox.itemconfig(i,{'bg': 'green'})

#------------------------------------- Name Input Page ----------------------------------------------------
#50音ボタンを押した時に呼ばれる関数
#コールバック関数をネストして定義
def jp_pressed(i, symbol, jp_entry):
    def x():
        #゛゜小が押された時の処理
        if i == 49:
            #置換用リスト
            sute_kana_check = ["ア", "イ", "ウ", "エ", "オ", "ツ", "ヤ", "ユ" , "ヨ", "ワ"]
            sute_kana = ["ァ", "ィ", "ゥ", "ェ", "ォ", "ッ", "ャ", "ュ", "ョ", "ヮ"]
            dull_check = ["カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ッ", "テ", "ト", "ハ", "ヒ", "フ", "ヘ", "ホ"]
            dull = ["ガ", "ギ", "グ", "ゲ", "ゴ", "ザ", "ジ", "ズ", "ゼ", "ゾ", "ダ", "ヂ", "ヅ", "デ", "ド", "バ", "ビ", "ブ", "ベ", "ボ"]
            p_list_check = ["バ", "ビ", "ブ", "ベ", "ボ"]
            p_list = ["パ", "ピ", "プ", "ペ", "ポ"]
            return_word_check = ["ァ", "ィ", "ゥ", "ェ", "ォ", "ガ", "ギ", "グ", "ゲ", "ゴ", "ザ", "ジ", "ズ", "ゼ", "ゾ", \
                                "ダ", "ヂ", "ヅ", "デ", "ド", "パ", "ピ", "プ", "ペ", "ポ", "ャ", "ュ", "ョ", "ヮ"]
            return_word = ["ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", \
                        "タ", "チ", "ツ", "テ", "ト", "ハ", "ヒ", "フ", "ヘ", "ホ", "ヤ", "ユ", "ヨ", "ワ"]

            #エントリーの取得
            word = jp_entry.get()
            #最後尾の単語を取得
            last_word = word[-1:]
            #置換を行うか判別するflag
            replace_flag = 0

            #捨て仮名への置換
            for j, sute in enumerate(sute_kana_check):
                if sute == last_word:
                    replace_word = sute_kana[j]
                    replace_flag = 1

            #濁音への置換
            for j, dull_word in enumerate(dull_check):
                if dull_word == last_word:
                    replace_word = dull[k]
                    replace_flag = 1

            #半濁音への置換
            for j, p in enumerate(p_list_check):
                if p == last_word:
                    replace_word = p_list[l]
                    replace_flag = 1

            #元の仮名への変換
            for j, re_word in enumerate(return_word_check):
                if re_word == last_word:
                    replace_word = return_word[m]
                    replace_flag = 1

            #replace_flagが立っている場合に置換を行う
            if replace_flag == 1:
                word = word[:-1]
                word = word + replace_word
                jp_entry.delete(0, tk.END)
                jp_entry.insert(tk.END, word)

        elif i != 36 or i !=38:
            jp_entry.insert(tk.END, symbol)
    return x

#1文字削除関数
def one_char_del(jp_entry):
    word = jp_entry.get()
    word = word[:-1]
    jp_entry.delete(0, tk.END)
    jp_entry.insert(tk.END, word)

def next_page(date_input_page, jp_entry):
    if len(jp_entry.get()) == 0:
        tkmsg.showwarning("showwarning", "商品名が入力されていません")
        return
    else:
        date_input_page.tkraise()

#キャンセルボタンが押された時に呼ばれる関数
def name_cancel(main_page, jp_entry):
    jp_entry.delete(0, tk.END)
    main_page.tkraise()

#------------------------------------- Date Input Page ----------------------------------------------------
#数字・クリア・xボタンが押された時の処理
#コールバック関数をネストして定義
def num_pressed(i, num, year_entry, month_entry, day_entry):
    def y():
        #どこまで日付が入力されているかの確認
        year = year_entry.get()
        year_len = len(year)
        month = month_entry.get()
        month_len = len(month)
        day = day_entry.get()
        day_len = len(day)
        #クリアボタン
        if i == 9:
            year_entry.delete(0, tk.END)
            month_entry.delete(0, tk.END)
            day_entry.delete(0, tk.END)

        #xボタン
        elif i == 11:
            if day_len >= 1:
                day = day[:-1]
                day_entry.delete(0, tk.END)
                day_entry.insert(tk.END, day)
            elif month_len >= 1:
                month = month[:-1]
                month_entry.delete(0, tk.END)
                month_entry.insert(tk.END, month)
            elif year_len >= 1:
                year = year[:-1]
                year_entry.delete(0, tk.END)
                year_entry.insert(tk.END, year)

        #0~9ボタン
        else:
            if (day_len == 1) or (month_len == 2 and day_len == 0):
                day_entry.insert(tk.END, num)
            elif (month_len == 1) or (year_len == 2 and month_len == 0):
                month_entry.insert(tk.END, num)
            elif year_len <= 1:
                year_entry.insert(tk.END, num)
    return y

#登録ボタンが押された時に呼ばれる関数
def register(stock, page, jp_entry, year_entry, month_entry, day_entry, var, sort_btn1, sort_btn2):
    #期限の読み込み
    year = int(year_entry.get())
    month = int(month_entry.get())
    day = int(day_entry.get())
    #期限が正しいか確認
    if month > 12 or month == 0:
        tkmsg.showwarning("showwarning", "月の入力が間違っています")
        month_entry.delete(0, tk.END)
        day_entry.delete(0, tk.END)
        return
    elif day > 31 or day == 0 or (day > 29 and month == 2) or (day > 30 and (month == 4 or month == 6 or month == 9 or month == 11)):#閏年は許して
        tkmsg.showwarning("showwarning", "日の入力が間違っています")
        day_entry.delete(0, tk.END)
        return
    #期限のエントリーをリセット
    year_entry.delete(0, tk.END)
    month_entry.delete(0, tk.END)
    day_entry.delete(0, tk.END)
    #商品名を読み込み
    item_name = jp_entry.get()
    jp_entry.delete(0, tk.END)
    #stockにデータを追加
    stock.append([item_name, datetime.date(2000 + year, month, day), 100])
    #Main Pageに遷移
    page.tkraise()
    #新規商品を加えて再び名称ソート
    name_sort(stock, var, sort_btn1, sort_btn2)
    sort_btn1.state(["pressed"])

#---------------------------------------- Edit Page -------------------------------------------------------
#削除ボタンが押された時に呼ばれる関数
def remove(stock, index, main_page, var, sort_btn1, sort_btn2):
    index = int(index.get())
    if len(stock) != 0:
        del stock[index]
        main_page.tkraise()
        name_sort(stock, var, sort_btn1, sort_btn2)
        sort_btn1.state(["pressed"])
    else:
        main_page.tkraise()
        name_sort(stock, var, sort_btn1, sort_btn2)
        sort_btn1.state(["pressed"])

#残量登録ボタンが押された時に呼ばれる関数
def residual(stock, index, main_page, var, sort_btn1, sort_btn2, radio_val):
    index = int(index.get())
    #残量の更新
    radio_val = radio_val.get()
    if radio_val == 0:
        stock[index][2] = 100
    elif radio_val == 1:
        stock[index][2] = 75
    elif radio_val == 2:
        stock[index][2] = 50
    elif radio_val == 3:
        stock[index][2] = 25
    #Main Pageに遷移
    main_page.tkraise()
    name_sort(stock, var, sort_btn1, sort_btn2)
    sort_btn1.state(["pressed"])

#------------------------------------- 複数ページで使用 ---------------------------------------------------
#ページ遷移用関数
def page_change(page):
    page.tkraise()

#==============================================================================================================
#main関数
#==============================================================================================================
def main() -> None:
    #ウィンドウ作成
    window = tk.Tk()
    #ウィンドウタイトル
    window.title(u"在庫管理")
    #ウィンドウサイズ
    window.geometry("800x600")
    #ウィンドウのグリッドを1x1に
    window.grid_rowconfigure(0, weight = 1)
    window.grid_columnconfigure(0, weight = 1)

    #在庫リストの動的確保
    stock = []
    #テスト用に値を代入
    stock.append(["リンゴ", datetime.date(2019, 1, 5), 100])
    stock.append(["ゴリラ", datetime.date(2019, 12, 30), 50])
    stock.append(["ラッパ", datetime.date(2019, 1, 8), 25])
    #編集用ラベル
    label = []

    #ttkのスタイルを設定
    style = ttk.Style()
    style.theme_use("alt")

    #----------------------------------------------------------------------------------------------------------
    #ページ遷移概要
    #ウィンドウの同じ位置に必要なページを配置し，ページの最上部を変更することでページ遷移を行う
    #                         Main Page
    #                  リスト↙︎       ↘︎+
    #              Edit Page           Name Input Page
    #   削除・キャンセル↓        キャンセル↓        ↘︎次へ
    #              Main Page            Main Page       Date Input Page
    #                                              キャンセル↓        ↘︎登録
    #                                                Name Input Page     Main Page
    #----------------------------------------------------------------------------------------------------------


    #------------------------------------------ Main Page -----------------------------------------------------
    #Main Page用のFrameを作成
    main_page = tk.Frame(window)

    #名称ソートボタンの設置
    sort_btn1 = ttk.Button(main_page, text = "名称ソート", command = lambda : name_sort(stock, var, sort_btn1, sort_btn2))
    sort_btn1.state(["pressed"])    #始めは名称ソートされたリストを表示
    sort_btn1.place(x = 0, width = 400, height = 30)

    #期限ソートボタンの設置
    sort_btn2 = ttk.Button(main_page, text = "期限ソート", command = lambda : deadline_sort(stock, var, sort_btn1, sort_btn2))
    sort_btn2.place(x = 400 , width = 400, height = 30)

    #リストボックス
    stock.sort(key = lambda x: x[0])
    name_list = []
    for i in range(len(stock)):
        name_list.append(stock[i][0] + "    日付:" + str(stock[i][1]) + "   残量:" + str(stock[i][2]) + "%")
    var = StringVar(value = name_list)
    listbox = tk.Listbox(main_page, listvariable = var)
    listbox.place(y = 30, width = 800, height = 570)
    coloring_list(stock,listbox) #消費期限による色付け

    #食材追加ボタンの設置
    add_btn = ttk.Button(main_page, text = "+", command = lambda : page_change(name_input_page))
    add_btn.place(x = 750, y = 550, width = 45, height = 45)

    #リストボックスのアイテム選択でlistbox_selectedを呼ぶ
    index = StringVar()
    listbox.bind("<<ListboxSelect>>", lambda event : listbox_selected(event, index, edit_page, item_label_text))

    #Main Pageを配置
    main_page.grid(row = 0, column = 0, sticky = "nsew")

    #------------------------------------------ Name Input Page ---------------------------------------------------
    #Name Input Page用のFrameを作成
    name_input_page = tk.Frame(window)

    #50音入力確認エントリー画面
    jp_entry = ttk.Entry(name_input_page, font = ("", 30))
    jp_entry.place(x = 100, y = 25, width = 600, height = 50)

    #50音入力ボタン
    japanese = ["ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ツ", "テ", \
                "ト", "ナ", "ニ", "ヌ", "ネ", "ノ", "ハ", "ヒ", "フ", "ヘ", "ホ", "マ", "ミ", "ム", "メ", "モ", "ヤ", "", "ユ", "", \
                "ヨ" , "ラ", "リ", "ル", "レ", "ロ", "ワ", "ヲ", "ン", "ー", " ゛　 ゜\n　 小"]
    jp_buttons = []
    for i, symbol in enumerate(japanese):
        jp_buttons.append(ttk.Button(name_input_page, text = symbol, command = jp_pressed(i, symbol, jp_entry)))
        x, y = divmod(i, 5)
        jp_buttons[i].place(x = x * 72, y = y * 80 + 100, width = 72, height = 80)

    #1文字削除ボタン
    char_del_btn = ttk.Button(name_input_page, text = "x", command = lambda : one_char_del(jp_entry))
    char_del_btn.place(x = 720, y = 100, width = 80, height = 200)

    #全文字削除ボタン
    all_del_btn = ttk.Button(name_input_page, text = "クリア", command = lambda : jp_entry.delete(0, tk.END))
    all_del_btn.place(x = 720, y = 300, width = 80, height = 200)

    #期限登録ページへの遷移ボタンの設置
    next_btn = ttk.Button(name_input_page, text = "次へ", command = lambda : next_page(date_input_page, jp_entry))
    next_btn.place(x = 0, y = 570, width = 400, height = 30)

    #キャンセルボタンの設置
    cancel_btn_Na = ttk.Button(name_input_page, text = "キャンセル", command = lambda : name_cancel(main_page, jp_entry))
    cancel_btn_Na.place(x = 400, y = 570, width = 400, height = 30)

    #Name Input Pageを配置
    name_input_page.grid(row = 0, column = 0, sticky = "nsew")

    #------------------------------------------ Date Input Page ---------------------------------------------------
    #Date Input Page用のFrameを作成
    date_input_page = tk.Frame(window)

    #期限(年)入力エントリーの設置
    twenty_label = tk.Label(date_input_page, font = ("", 30), text = "20")
    twenty_label.place(x = 235, y = 30)
    year_entry = ttk.Entry(date_input_page, font = ("", 30))
    year_entry.place(x = 275, y = 25, width = 50, height = 50)
    #year_entry.focus_set()
    year_label = tk.Label(date_input_page, font = ("", 30), text = "年")
    year_label.place(x = 325, y = 30)

    #期限(月)入力エントリーの設置
    month_entry = ttk.Entry(date_input_page, font = ("", 30))
    month_entry.place(x = 375, y = 25, width = 50, height = 50)
    month_label = tk.Label(date_input_page, font = ("", 30), text = "月")
    month_label.place(x = 425, y = 30)

    #期限(日)入力エントリーの設置
    day_entry = ttk.Entry(date_input_page, font = ("", 30))
    day_entry.place(x = 475, y = 25, width = 50, height = 50)
    day_label = tk.Label(date_input_page, font = ("", 30), text = "日")
    day_label.place(x = 525, y = 30)

    #期限入力用数字ボタン
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, "クリア", 0, "x"]
    num_buttons = []
    for i, num in enumerate(num_list):
        num_buttons.append(ttk.Button(date_input_page, text = num, command = num_pressed(i, num, year_entry, month_entry, day_entry)))
        y, x = divmod(i, 3)
        num_buttons[i].place(x = 100 * x + 250, y = 100 * y + 150, width = 100, height = 100)

    #次の商品を登録するボタンの設置
    register_next_btn = ttk.Button(date_input_page, text = "他の商品を登録する", command = lambda : register(stock, name_input_page, \
                                                                        jp_entry, year_entry, month_entry, day_entry, var, sort_btn1, sort_btn2))
    register_next_btn.place(x = 0, y = 570, width = 300, height = 30)

    #登録ボタンの設置
    register_btn = ttk.Button(date_input_page, text = "登録", command = lambda : register(stock, main_page, jp_entry, year_entry,\
                                                                            month_entry, day_entry, var, sort_btn1, sort_btn2))
    register_btn.place(x = 300, y = 570, width = 300, height = 30)

    #キャンセルボタンの設置
    cancel_btn_In = ttk.Button(date_input_page, text = "キャンセル", command = lambda : page_change(name_input_page))
    cancel_btn_In.place(x = 600, y = 570, width = 200, height = 30)

    #Date Input Pageを配置
    date_input_page.grid(row = 0, column = 0, sticky = "nsew")

    #------------------------------------------ Edit Page ----------------------------------------------------
    #Edit Page用のFrameを作成
    edit_page = tk.Frame(window)

    #商品データラベルの作成
    item_label_text = tk.StringVar()
    item_label = tk.Label(edit_page, font = ("", 30), textvariable = item_label_text)
    item_label.pack()

    #残量ボタン(25%刻み)の設置
    #画像に線を引いて入力する場合はラジオボタンの位置を適当に変える
    radio_val = tk.IntVar()
    radio_val.set(0)

    #100%ボタンの設置
    full_btn = tk.Radiobutton(edit_page, font = ("", 30), text = "100%", variable = radio_val, value = 0)
    full_btn.place(x = 600, y = 280)

    #75%ボタンの設置
    three_quarter_btn = tk.Radiobutton(edit_page, font = ("", 30), text = "75%", variable = radio_val, value = 1)
    three_quarter_btn.place(x = 400, y = 280)

    #50%ボタンの設置
    half_btn = tk.Radiobutton(edit_page, font = ("", 30), text = "50%", variable = radio_val, value = 2)
    half_btn.place(x = 200, y = 280)

    #25%ボタンの設置
    quarter_btn = tk.Radiobutton(edit_page, font = ("", 30), text = "25%", variable = radio_val, value = 3)
    quarter_btn.place(x = 0, y = 280)

    #削除ボタンの設置
    rm_btn = ttk.Button(edit_page, text = "削除", command = lambda : remove(stock, index, main_page, var, sort_btn1, sort_btn2))
    rm_btn.place(x = 0, y = 570, width = 300, height = 30)

    #残量登録ボタンの設置
    res_btn = ttk.Button(edit_page, text = "残量登録", command = lambda : residual(stock, index, main_page, var, sort_btn1, sort_btn2, radio_val))
    res_btn.place(x = 300, y = 570, width = 300, height = 30)

    #キャンセルボタンの設置
    cancel_btn_Ed = ttk.Button(edit_page, text = "キャンセル", command = lambda : page_change(main_page))
    cancel_btn_Ed.place(x = 600, y = 570, width = 200, height = 30)

    #Edit Pageを配置
    edit_page.grid(row = 0, column = 0, sticky = "nsew")

    #------------------------------------- プログラムの開始 ---------------------------------------------------
    #Main Pageを最上位に表示
    main_page.tkraise()
    #edit_page.tkraise()
    window.mainloop()

#==============================================================================================================
#本体処理
#==============================================================================================================
if __name__ == "__main__":
    main()
