from functools import partial
import maya.cmds as cmds
import json

class MayaRenameTool:
    def __init__(self):
        self.name_data = []
        
    def load(self):
        self.name_data = cmds.ls(sl=True)
        
    def rename_sl(self,prefix):
        for num,name in enumerate(self.name_data):
            new_name = f"{prefix}{num+1:03d}"
            cmds.rename(name,new_name)

class PresetManager:
    def __init__(self,filename):
        self.filename = filename
        self.presets =[]
        
    def add_preset(self,prefix):
        self.presets.append(prefix)
        
    def save(self):
        with open(self.filename,"w",encoding="utf-8")as f:
            json.dump(self.presets,f,ensure_ascii=False,indent=2)
        print("プリセットに保存しました")
            
    def load(self):
        try:
            with open(self.filename,"r",encoding="utf-8")as f:
                self.presets = json.load(f)
            print("プリセットを読み込みました")
        except FileNotFoundError:
            print("プリセットがファイルが存在しません")
            self.presets = []
        return self.presets

def on_click(*args):
    prefix_text = cmds.textField(field,query = True,text = True)
    renametool.rename_sl(prefix_text)

def on_click_preset(*args):
    preset_text = cmds.textField(field,query = True,text = True)
    presetmanager.add_preset(preset_text)
    presetmanager.save()

def apply_preset(preset_name, *args):
    cmds.textField(field, edit=True, text=preset_name)

def show_window():
    global renametool,field,presetmanager
    renametool = MayaRenameTool()
    Path = r"C:\python_py\python-practice\06-02-python\presets.json"
    presetmanager = PresetManager(Path)
    presets = presetmanager.load()



    ToolName = "renametl"
    if cmds.window(ToolName,exists=True):
        cmds.deleteUI(ToolName)

    window = cmds.window(ToolName,title="選択対象リネームツール",widthHeight=(300,100))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="リネームする際に着けるプレフィックスを書いてください")
    cmds.text(label="プリセット内のプレフィックス")
    for i in presets:
        cmds.button(label=i, command=partial(apply_preset, i))

    field = cmds.textField()
    cmds.button(label="リネーム",command=on_click),cmds.button(label="プリセット保存",command=on_click_preset)
    cmds.showWindow(window)

            
### 
renametool = MayaRenameTool()     
Path = (r"C:\python_py\python-practice\06-02-python\presets.json")
            

preset =  PresetManager(Path)   

preset.load()
print(f"保存されているプリセット：{preset.presets}")

renametool.load()
renametool.rename_sl(preset.presets[0])
###
