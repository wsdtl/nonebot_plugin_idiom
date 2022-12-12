import pandas as pd
import numpy as np
import os
from pathlib import Path
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

__plugin_meta__ = PluginMetadata(
    name="成语接龙",
    description="来和机器人玩成语接龙吧！！！",
    usage=(
        "来机器人玩成语接龙吧！指令： < 成语接龙 | 成语接龙 + 一个成语 >"
    )
)

files = Path() / os.path.dirname(__file__) / "idiom.json"

idiom = pd.read_json(files)
t = idiom.pinyin.str.split()
idiom["firstChar"] = t.str[0]
idiom["lastChar"] = t.str[-1]
idiom = idiom.set_index("word")[["firstChar", "lastChar"]]
word2 = ""
lastChar = ""
resp_sentence = ["太厉害了",
                 "竟然被你答上来了",
                 "你简直是个文学家",
                 "你很棒哦",
                 "开始佩服你了呢"]

chen_yu = on_command('成语接龙', aliases={'接龙'}, priority=12, block=True)


@chen_yu.handle()
async def chen_yu_(event: MessageEvent, state: T_State, msg: Message = CommandArg()):
    global idiom
    global word2
    global lastChar
    msg = msg.extract_plain_text().strip()
    if msg:
        if msg not in idiom.index:
            word2 = np.random.choice(idiom.index)
            await chen_yu.send("你输入的不是一个成语，那我就先开始啦，接招：【" + word2 + "】，认输或者不想玩了记得告诉我:< 不玩了|取消 >哦！！")
        else:
            words = idiom.index[idiom.firstChar == idiom.loc[msg, "lastChar"]]
            word2 = np.random.choice(words)
            if msg[-1] != word2[0]:
                words = idiom.index[idiom.firstChar == idiom.loc[msg, "lastChar"]]
                word2 = np.random.choice(words)
                if msg[-1] != word2[0]:
                    await chen_yu.finish("恭喜你赢了！你太厉害了，开局我就被你打败了，好不甘心！！！")
            lastChar = idiom.loc[word2, "lastChar"]
            await chen_yu.send("接招!我的答案是【" + word2 + "】，认输或者不想玩了记得告诉我:< 不玩了|取消 >哦！")

    else:
        word2 = np.random.choice(idiom.index)
        lastChar = idiom.loc[word2, "lastChar"]
        await chen_yu.send('那我就先开始啦，接招：【' + word2 + '】，认输或者不想玩了记得告诉我:< 不玩了|取消 >哦！')


@chen_yu.got('text', prompt='')
async def chen_yu_got_(event: MessageEvent, state: T_State):
    global idiom
    global word2
    global lastChar
    tp = state["text"].extract_plain_text().strip()
    if tp == "不玩了" or tp == "取消":
        await chen_yu.finish("好的，游戏结束啦，欢迎下次来玩哦~！")
    else:
        if tp not in idiom.index:
            await chen_yu.reject("你输入的不是一个成语，请重新输入！")
        elif lastChar and idiom.loc[tp, 'firstChar'] != lastChar:
            await chen_yu.finish("哈哈，你的答案错了，我赢啦，游戏结束！！！")
        elif idiom.index[idiom.firstChar == idiom.loc[tp, "lastChar"]].shape[0] == 0:
            await chen_yu.finish("恭喜你赢了！你太厉害了，我被你打败！！！")
        else:
            words = idiom.index[idiom.firstChar == idiom.loc[tp, "lastChar"]]
            word2 = np.random.choice(words)
            if tp[-1] != word2[0]:
                words = idiom.index[idiom.firstChar == idiom.loc[tp, "lastChar"]]
                word2 = np.random.choice(words)
                if tp[-1] != word2[0]:
                    await chen_yu.finish("恭喜你赢了！你太厉害了，我被你打败！！！")
            lastChar = idiom.loc[word2, "lastChar"]
            await chen_yu.reject(np.random.choice(resp_sentence) + "，我的答案是【" + word2 + "】")


