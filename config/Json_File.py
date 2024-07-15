import json
import os
pet = {
    "width": 98,              #所有 PNG 图片的最大宽度
    "height": 98,             #所有 PNG 图片的最大高度
    "scale": 1.0,             #图片显示比例，会影响宠物大小、单位时间移动距离
    
    "refresh": 5,             #动画模块随机显示动作之间的时间间隔，单位为 s
    "interact_speed":0.02,    #交互模块的响应刷新间隔，0.02s 是较为理想的间隔，不需要在素材开发时修改

    "default": "default",     #此处定义了一些必要动作
    "up": "up",               #但目前只有 default、drag、fall 真正用到
    "down": "down",           #其他的只是为以后版本拓展所做的拓展
    "left": "left",           #目前可以全都用 default 动作代替
    "right": "right",
    "drag": "drag",           #用法例："default": "angry"
    "fall": "fall",           #定义 default 动作为 动作参数文件中 名为 "angry" 的动作
    
    #random_act 定义了一系列动作组，用于在动画模块中随机展示，或在右键菜单中选择进行展示
    "random_act": [
        {"name":"stand", "act_list":["default"], "act_prob":1.0, "act_type":[2,0]},
        {"name":"walk", "act_list":["left_walk", "right_walk","default"], "act_prob":0.1, "act_type":[3,1]},
        {"name":"angry", "act_list":["angry"], "act_prob":1.0, "act_type":[0,0]},
        {"name":"sleep", "act_list":["fall_asleep", "sleep"], "act_prob":0.05, "act_type":[1,1]},
        {"name":"on_floor", "act_list":["on_floor"], "act_prob":0, "act_type":[0,10000]},
        {"name":"think", "act_list":["think", "sad"], "act_prob":0.5, "act_type":[1,1]}
    ],
    
    #accessory_act 定义了一系列拥有组件的动作，在右键菜单中选择进行展示
    "accessory_act":[
        {"name":"XXX", "act_list":["XXX"], "acc_list":["XXX"], "act_type":[2,1],
        "follow_mouse": True, "above_main":False, "anchor":[145,145]}
    ],
    
    #宠物自定义的物品喜爱度 （特别喜欢 / 一般 / 讨厌）
    "item_favorite": {"meats": 2.0, "chips":1.5, "hamburgers":2.0, "coke":1.5}, # 物品名称：好感度倍率
    "item_dislike": {"vegetables": 0.5}
}

pet_object = json.dumps(pet, indent=16)
with open("config.json", "w") as outfile:
    outfile.write(pet_object)