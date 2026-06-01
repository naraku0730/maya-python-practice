
import maya.cmds as cmds

def on_click(*args):
    name = cmds.textField(name_field,query = True,text = True)
    cmds.sphere(name=name)
    print(f"{name}を作成しました")

if cmds.window("myTool", exists=True):
    cmds.deleteUI("myTool")
window = cmds.window("myTool",title="球体作成ツール",widthHeight=(300,100))
cmds.columnLayout(adjustableColumn=True)
cmds.text(label="作成する球体に付ける名前をかいてください")
name_field = cmds.textField()
cmds.button(label="作成",command=on_click)
cmds.showWindow(window)