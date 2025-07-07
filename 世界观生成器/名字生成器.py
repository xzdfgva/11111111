import random
import csv
import os

# 预设风格数据
styles = {
    "人名": {
        "奇幻": {
            "syllables": ["ar", "el", "dor", "mir", "an", "th", "ion", "is", "val", "ser", "lin", "gal", "fen", "lor", "sil", "tir"],
            "meanings": ["光明", "森林", "勇士", "智慧", "守护", "魔法", "王者", "信仰", "山谷", "星辰", "精灵", "圣地", "风暴", "荣耀", "银色", "高地"],
            "pronunciation": ["a", "e", "dɔr", "miːr", "æn", "θ", "iːɔn", "is", "væl", "sɛr", "lin", "gal", "fɛn", "lɔr", "sil", "tir"]
        },
        "科幻": {
            "syllables": ["xen", "zor", "tek", "qu", "ly", "ron", "cy", "va", "neo", "astra", "plex", "zeno", "vex", "tron", "byte", "nova"],
            "meanings": ["未来", "机械", "星际", "智能", "探索", "能量", "虚拟", "速度", "新", "星际", "复合", "异域", "能量", "电子", "字节", "新星"],
            "pronunciation": ["zen", "zɔr", "tɛk", "kjuː", "li", "rɔn", "saɪ", "va", "niːo", "æstrə", "pleks", "zeno", "veks", "trɒn", "baɪt", "novə"]
        },
        "古风": {
            "syllables": ["云", "霜", "凌", "轩", "瑶", "墨", "竹", "寒", "青", "岚", "澈", "宸", "渊", "烨", "尘", "笙"],
            "meanings": ["高远", "清冷", "俊逸", "雅致", "美玉", "文雅", "坚韧", "冷静", "青翠", "山雾", "清澈", "天宇", "深远", "光辉", "尘世", "乐音"],
            "pronunciation": ["yún", "shuāng", "líng", "xuān", "yáo", "mò", "zhú", "hán", "qīng", "lán", "chè", "chén", "yuān", "yè", "chén", "shēng"]
        }
    },
    "地名": {
        "奇幻": {
            "syllables": ["val", "nor", "sil", "tir", "gal", "mor", "fel", "lun", "eld", "drak", "rune", "thal", "mir", "sol", "bar", "dun"],
            "meanings": ["山谷", "北境", "银色", "高地", "圣地", "黑暗", "幸运", "月亮", "古树", "巨龙", "符文", "王座", "湖泊", "太阳", "石堡", "深渊"],
            "pronunciation": ["væl", "nɔr", "sil", "tir", "gal", "mɔr", "fel", "lun", "ɛld", "dræk", "ruːn", "θæl", "mir", "sɒl", "bɑr", "dʌn"]
        },
        "科幻": {
            "syllables": ["neo", "astra", "terra", "cyber", "nova", "plex", "zeno", "vex", "quant", "orbit", "luna", "core", "matrix", "ion", "star", "pulse"],
            "meanings": ["新", "星际", "地球", "赛博", "新星", "复合", "异域", "能量", "量子", "轨道", "月球", "核心", "矩阵", "离子", "恒星", "脉冲"],
            "pronunciation": ["niːo", "æstrə", "terə", "saɪbər", "novə", "pleks", "zeno", "veks", "kwɒnt", "ɔːbɪt", "luːnə", "kɔːr", "meɪtrɪks", "aɪɒn", "stɑr", "pʌls"]
        },
        "古风": {
            "syllables": ["长安", "洛", "幽", "苍", "青", "云", "溪", "岭", "渔", "松", "澜", "岱", "潇", "雁", "枫", "澜"],
            "meanings": ["永恒", "水边", "幽静", "苍茫", "青翠", "高远", "溪流", "山岭", "渔村", "松林", "大浪", "高山", "潇洒", "归雁", "枫林", "波澜"],
            "pronunciation": ["cháng ān", "luò", "yōu", "cāng", "qīng", "yún", "xī", "lǐng", "yú", "sōng", "lán", "dài", "xiāo", "yàn", "fēng", "lán"]
        }
    }
}

def get_db_file(name_type):
    return f"{name_type}_db.csv"

def load_db(db_file):
    if not os.path.exists(db_file):
        return set()
    with open(db_file, newline='', encoding='utf-8') as f:
        return set(row[0] for row in csv.reader(f))

def save_to_db(db_file, name):
    with open(db_file, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([name])

def generate_name(name_type, style):
    data = styles[name_type][style]
    db_file = get_db_file(name_type)
    db = load_db(db_file)
    tries = 0
    while tries < 100:
        idxs = random.sample(range(len(data["syllables"])), 2)
        name = data["syllables"][idxs[0]].capitalize() + data["syllables"][idxs[1]]
        meaning = data["meanings"][idxs[0]] + "·" + data["meanings"][idxs[1]]
        pronunciation = data["pronunciation"][idxs[0]] + "-" + data["pronunciation"][idxs[1]]
        if name not in db:
            save_to_db(db_file, name)
            return name, meaning, pronunciation
        tries += 1
    return None, None, None

if __name__ == "__main__":
    while True:
        print("请选择类型：1.人名 2.地名 (输入q退出)")
        type_choice = input("输入数字选择类型：")
        if type_choice.lower() == 'q':
            print("已退出生成器。")
            break
        type_map = {"1": "人名", "2": "地名"}
        name_type = type_map.get(type_choice, "人名")
        print("请选择风格：1.奇幻 2.科幻 3.古风 (输入q返回上一级)")
        style_choice = input("输入数字选择风格：")
        if style_choice.lower() == 'q':
            continue
        style_map = {"1": "奇幻", "2": "科幻", "3": "古风"}
        style = style_map.get(style_choice, "奇幻")
        name, meaning, pronunciation = generate_name(name_type, style)
        if name:
            print(f"生成的{name_type}：{name}")
            print(f"含义：{meaning}")
            print(f"发音指南：{pronunciation}")
        else:
            print("未能生成新名字，请重试或扩展数据库。")
        print("-----------------------------")