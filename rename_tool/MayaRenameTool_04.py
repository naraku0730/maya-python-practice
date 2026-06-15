from functools import partial
import maya.cmds as cmds
import json
#リネーム担当のクラス
class MayaRenameTool:
    #空のリネーム対象のリストを作る
    def __init__(self):
        self.name_data = []
        
    #選択しているものを読みとりリストに入れる
    def load(self):
        self.name_data = cmds.ls(sl=True)
        
    #リスト内のオブジェクトにプリフィックス＋3桁のナンバリングの名前にリネームする
    def rename_sl(self,prefix):
        if not self.name_data:
            print("選択されていません")
            return
        for num,name in enumerate(self.name_data):
            new_name = f"{prefix}{num+1:03d}"
            cmds.rename(name,new_name)
#プリフィックスをプリセットに保存するクラス
class PresetManager:
    #ファイル名（パス）をいれて保存場所を決める、プリフィックスを保存する空のリストを作る
    def __init__(self,filename):
        self.filename = filename
        self.presets =[]
        
    #引数のプリフィックスをプリセットにする
    def add_preset(self,prefix):
        if prefix in self.presets:
            print("すでにプリセットに保存されています")
            return
        self.presets.append(prefix)
        
    #プリセットの中から指定のインデックスのプリフィックスを削除しJSONファイルに保存する
    def delete_preset(self,index):
        del_str = self.presets.pop(index)
        print(f"{del_str}を削除しました")
        self.save()
        
    #プリセットのリストをJSONファイルに保存する
    def save(self):
        with open(self.filename,"w",encoding="utf-8")as f:
            json.dump(self.presets,f,ensure_ascii=False,indent=2)
        print("プリセットに保存しました")
            
    #プリセットのリストにJSONファイルに保存したプリセットをロードし値を返す、ファイルが見つからなければ空のリストを返す
    def load(self):
        try:
            with open(self.filename,"r",encoding="utf-8")as f:
                self.presets = json.load(f)
            print("プリセットを読み込みました")
        except FileNotFoundError:
            print("プリセットがファイルが存在しません")
            self.presets = []
        return self.presets

#リネームボタンでon_clickが呼ばれた際に入力内容を取得し、選択対象をロードしリネームする
def on_click(*args):
    prefix_text = cmds.textField(field,query = True,text = True)
    if not prefix_text:
        print("入力欄に何も入力されていません")
        return
    renametool.load()
    renametool.rename_sl(prefix_text)

#プリセット保存ボタンでon_click_presetを呼び出し、入力内容を取得し、プリセットに追加しJSONに保存
def on_click_preset(*args):
    preset_text = cmds.textField(field,query = True,text = True)
    if not preset_text:
        print("入力欄に何も入力されていません")
        return
    presetmanager.add_preset(preset_text)
    presetmanager.save()
    cmds.evalDeferred(show_window)

#プリセットボタンでapply_presetを呼び出し、partialで渡されたpresetを入力欄に書き込む。
def apply_preset(preset_name, *args):
    cmds.textField(field, edit=True, text=preset_name)
    
def delete_pre(index,*args):
    presetmanager.delete_preset(index)
    cmds.evalDeferred(show_window)
    

#メインの処理、画面に関する処理　globalでインスタンスを他クラスでも使えるようにする
def show_window():
    global renametool,field,presetmanager
    renametool = MayaRenameTool()
    Path = r"C:\python_py\python-practice\06-02-python\presets.json"
    presetmanager = PresetManager(Path)
    presets = presetmanager.load()


    #windowIDを定数化すでに同じウィンドウを開いていたら削除
    ToolName = "renametl"
    if cmds.window(ToolName,exists=True):
        cmds.deleteUI(ToolName)

    #ウィンドウを作成し、表示を縦に並べるレイアウト
    window = cmds.window(ToolName,title="選択対象リネームツール",widthHeight=(300,500))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="リネームする際に着けるプレフィックスを書いてください")
    cmds.text(label="プリセット内のプレフィックス")
    
    #横並びのレイアウトに変更
    for i ,name in enumerate(presets):
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label = name ,command=partial(apply_preset,name))
        cmds.button(label = "削除",command=partial(delete_pre,i))
        cmds.setParent("..")#横並びのレイアウト終了、縦並びに移行

    #入力欄をfieldにいれる
    field = cmds.textField()
   
    cmds.button(label="リネーム",command=on_click)
    cmds.button(label="プリセット保存",command=on_click_preset)
    cmds.showWindow(window)

show_window()
