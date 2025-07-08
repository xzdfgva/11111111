import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import random
import datetime
import os
import json

class EnhancedWorldGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("高级世界观生成器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 初始化数据存储
        self.history = []
        self.favorites = []
        self.load_data()
        
        # 设置样式
        self.setup_styles()
        
        # 扩展的风格选项
        self.styles = {
            "人名": {
                "奇幻": [
                    "阿尔维斯", "贝伦加尔", "塞德里克", "迪兰", "埃德里克", "法伦", "加文", "哈罗德", 
                    "伊恩", "杰兰特", "凯斯宾", "莱昂纳德", "马格努斯", "奈杰尔", "奥利弗", "珀西瓦尔", 
                    "昆汀", "罗兰", "塞巴斯蒂安", "特伦斯", "乌瑟尔", "维克多", "沃尔夫冈", "泽维尔",
                    "阿瓦隆", "布里安娜", "塞勒涅", "黛安娜", "伊莎贝拉", "芙蕾雅", "加利亚", "海伦娜", 
                    "伊莫金", "吉安娜", "卡珊德拉", "莱拉", "梅芙", "妮莎", "奥罗拉", "珀涅罗珀", 
                    "昆蒂拉", "蕾拉", "西尔维娅", "塔玛拉", "乌娜", "维维安", "温妮弗雷德", "赞茜"
                ],
                "科幻": [
                    "阿尔法", "巴克斯", "赛昂", "德尔塔", "伊普西隆", "菲尼克斯", "伽马", "伊卡洛斯", 
                    "朱诺", "凯隆", "利维坦", "缪斯", "诺瓦", "欧米茄", "普罗米修斯", "量子", "拉", 
                    "西格玛", "泰坦", "尤尼恩", "伏尔甘", "怀尔德", "泽塔", "零", "艾柯", "比特",
                    "艾丽塔", "贝塔", "卡利斯托", "达芙妮", "伊芙", "费莉西亚", "盖亚", "赫拉", 
                    "艾莎", "卡门", "莱拉", "玛雅", "尼芙", "奥罗拉", "菲比", "奎莎", "瑞亚", 
                    "斯塔", "塔利亚", "尤妮斯", "薇拉", "西风", "雅娜", "佐伊", "艾克斯", "诺娃"
                ],
                "古风": [
                    "安之", "北冥", "长庚", "承煜", "德昭", "观澜", "浩然", "弘毅", "景行", "俊彦", 
                    "开宇", "乐康", "明远", "墨宸", "南枝", "清远", "思齐", "天翊", "修远", "玄烨", 
                    "彦博", "翊晨", "煜城", "致远", "子衿", "子墨", "子轩",
                    "安澜", "初瑶", "楚怀", "丹青", "蝶衣", "芙蕖", "顾盼", "海棠", "蕙质", "静姝", 
                    "兰芷", "灵犀", "妙菡", "南笙", "清婉", "如烟", "若雪", "诗涵", "书瑶", "水墨", 
                    "晚晴", "未央", "湘灵", "心远", "嫣然", "云岫", "知夏"
                ],
                "蒸汽朋克": [
                    "阿彻", "巴纳比", "克拉伦斯", "德克斯特", "伊桑", "芬奇", "加百列", "霍雷肖", 
                    "以斯拉", "杰里科", "凯斯", "勒罗伊", "迈尔斯", "内森", "奥古斯塔斯", "珀西", 
                    "昆西", "莱利", "斯特林", "西奥多", "乌利亚", "瓦伦丁", "温斯顿", "泽克", "亚伯",
                    "阿达", "碧翠丝", "塞西莉", "黛西", "伊莎朵拉", "范妮", "格蕾丝", "赫敏", 
                    "伊莫金", "约瑟芬", "凯瑟琳", "莉莲", "玛蒂尔达", "诺拉", "奥克塔维亚", "波莉", 
                    "奎妮", "露丝", "塞拉菲娜", "塔比莎", "尤多拉", "维奥莱特", "温妮", "泽尔达", "艾达"
                ],
                "赛博朋克": [
                    "阿克塞尔", "刀锋", "眼镜蛇", "德雷克", "电子", "闪回", "黑客", "霓虹", "奥术", 
                    "脉冲", "雷诺", "赛博", "轨道", "毒刺", "涡轮", "幽灵", "瓦砾", "X", "零号", "狂怒",
                    "阿尔法", "比特", "赛博", "迪斯科", "伊芙", "火焰", "齿轮", "ハーレム", "冰", 
                    "杰特", "克莉丝", "闪电", "霓虹", "奥克塔", "菲尼克斯", "量子", "拉文", "风暴", 
                    "毒素", "尤妮克", "薇克斯", "西风", "雅努斯", "泽塔", "零", "狂想", "艾柯"
                ]
            },
            "地名": {
                "奇幻": [
                    "艾森加德", "贝奥恩伍德", "卡拉斯加拉顿", "暗影裂隙", "埃瑞德路因", "风息堡", "灰谷", 
                    "希尔斯布莱德", "铁炉堡", "翡翠林", "吉尔尼斯", "黑石山", "冰冠冰川", "卡拉赞", 
                    "诺森德", "奥格瑞玛", "潘达利亚", "奎尔萨拉斯", "瑞文戴尔", "石爪山脉", "索瑞森", 
                    "泰达希尔", "厄运之槌", "瓦丝琪尔", "幽魂之地", "祖阿曼", "永歌森林",
                    "阿瓦隆", "布罗塞尔", "卡米洛特", "达戈拉德", "埃尔多拉多", "风行者", "格瑞姆巴托", 
                    "黑海岸", "铁壁堡垒", "翡翠梦境", "吉尔尼斯", "黑石山", "冰冠冰川", "卡拉赞", 
                    "诺森德", "奥格瑞玛", "潘达利亚", "奎尔萨拉斯", "瑞文戴尔", "石爪山脉", "索瑞森", 
                    "泰达希尔", "厄运之槌", "瓦丝琪尔", "幽魂之地", "祖阿曼", "永歌森林"
                ],
                "科幻": [
                    "阿尔法象限", "巴别塔", "赛博空间", "德尔塔基地", "欧米茄中心", "未来之城", "银河联邦", 
                    "星际之门", "杰格城", "卡帕星", "拉格朗日点", "火星殖民地", "新纽约", "奥米伽基地", 
                    "凤凰城", "量子领域", "辐射区", "赛博坦", "泰坦星", "尤尼恩城", "瓦尔哈拉", "零点地带", 
                    "泽塔殖民地", "阿克隆", "巴洛特", "赛博朋克城", "达卡", "伊卡洛斯", "菲尼克斯", 
                    "盖亚", "海伯利安", "伊卡洛斯", "朱诺", "凯隆", "利维坦", "缪斯", "诺瓦", "欧米茄"
                ],
                "古风": [
                    "长安", "洛阳", "姑苏", "金陵", "临安", "幽州", "青城", "云梦泽", "白帝城", "雁门关", 
                    "桃花源", "蓬莱岛", "昆仑墟", "终南山", "武夷山", "滕王阁", "黄鹤楼", "岳阳楼", 
                    "寒山寺", "少林寺", "峨眉山", "武当山", "青城山", "龙虎山", "丹霞山", "九华山", 
                    "普陀山", "雁荡山", "黄山", "庐山", "泰山", "衡山", "华山", "恒山", "嵩山"
                ],
                "蒸汽朋克": [
                    "齿轮城", "飞艇港", "蒸汽堡", "发条镇", "铜管巷", "黄铜塔", "烟囱区", "维多利亚站", 
                    "黑煤窑", "铁砧广场", "蒸汽工厂", "齿轮迷宫", "发条森林", "蒸汽铁路", "黄铜集市", 
                    "烟囱峡谷", "维多利亚港", "黑煤窑", "铁砧广场", "蒸汽工厂", "齿轮迷宫", "发条森林", 
                    "蒸汽铁路", "黄铜集市", "烟囱峡谷", "维多利亚港", "黑煤窑", "铁砧广场", "蒸汽工厂"
                ],
                "赛博朋克": [
                    "夜之城", "九龙寨城", "霓虹区", "数据港", "公司塔", "下层区", "天空城", "网络空间", 
                    "垃圾场", "义体诊所", "黑客区", "红砂区", "霓虹大道", "数据流", "企业区", "贫民窟", 
                    "浮空城", "虚拟世界", "黑入点", "赛博坟场", "神经商城", "基因库", "纳米工厂", 
                    "记忆诊所", "广告塔", "霓虹瀑布", "数据流", "企业区", "贫民窟", "浮空城", "虚拟世界"
                ]
            }
        }
        
        # 含义数据
        self.meanings = {
            "人名": {
                "奇幻": [
                    "光明使者", "森林守护者", "龙之友", "精灵王子", "矮人战士", "人类国王", "白袍巫师", "黑暗法师",
                    "元素掌控者", "魔法学徒", "亡灵法师", "圣骑士", "游侠", "德鲁伊", "刺客", "吟游诗人",
                    "炼金术士", "预言者", "召唤师", "巫医", "圣骑士", "龙骑士", "血法师", "暗影猎手", "符文大师"
                ],
                "科幻": [
                    "救世主", "黑客", "船长", "特工", "工程师", "科学家", "机器人", "量子物理学家",
                    "星际走私者", "太空海盗", "基因改造人", "人工智能", "机械师", "宇航员", "武器专家", "数据分析师",
                    "生物学家", "电子工程师", "纳米技术专家", "时空旅行者", "星际外交官", "赛博格", "神经科学家", "能量武器专家"
                ],
                "古风": [
                    "高洁之士", "冷峻剑客", "文雅书生", "山间隐士", "美玉佳人", "寒夜孤星", "竹下君子", "皇家贵胄",
                    "江湖豪侠", "大内高手", "书香门第", "神医圣手", "诗画双绝", "琴棋名家", "茶道宗师", "剑术大师",
                    "谋士智囊", "忠勇将军", "铁血刺客", "妙手神偷", "江湖游侠", "世外高人", "隐世富豪", "才女佳人"
                ],
                "蒸汽朋克": [
                    "发明家", "飞艇船长", "机械师", "贵族小姐", "工业大亨", "探险家", "钟表匠", "秘密特工",
                    "蒸汽工程师", "齿轮工匠", "热气球驾驶员", "铁路大亨", "电报员", "机械守卫", "蒸汽医生", "发条技师",
                    "炼金术士", "蒸汽骑士", "齿轮法师", "蒸汽朋克", "工业间谍", "机械设计师", "蒸汽朋克", "发条刺客"
                ],
                "赛博朋克": [
                    "网络黑客", "街头佣兵", "公司特工", "义体医生", "媒体人", "帮派成员", "AI实体", "赛博忍者",
                    "神经漫游者", "赛博侦探", "义体改造师", "数据掮客", "基因编辑师", "霓虹舞者", "记忆贩子", "广告墙艺术家",
                    "赛博格战士", "网络安全专家", "虚拟现实设计师", "赛博朋克", "神经科学家", "纳米技术专家", "赛博朋克", "赛博诗人"
                ]
            },
            "地名": {
                "奇幻": [
                    "精灵的故乡", "风暴聚集之地", "巨龙栖息处", "远古森林", "矮人的家园", "被遗忘的王国", "神圣殿堂", "邪恶深渊",
                    "魔法能量中心", "亡灵之地", "元素平原", "巨龙巢穴", "精灵圣地", "矮人矿脉", "巫师塔群", "恶魔领地",
                    "天使之城", "龙族禁地", "巨人国度", "妖精森林", "亡灵国度", "元素神殿", "龙眠之地", "精灵之森"
                ],
                "科幻": [
                    "未来之城", "虚拟世界", "科研中心", "星际枢纽", "计算机核心", "太空站", "月球基地", "火星殖民地",
                    "基因实验室", "量子研究所", "宇宙监狱", "星际港口", "太空殖民地", "外星遗迹", "能量核心", "时间研究所",
                    "克隆工厂", "纳米技术中心", "虚拟现实工厂", "赛博格改造中心", "神经科学研究所", "人工智能孵化场", "量子计算中心", "太空城"
                ],
                "古风": [
                    "永恒之都", "牡丹之城", "江南水乡", "六朝古都", "南宋都城", "北方重镇", "道教圣地", "云梦大泽",
                    "武林圣地", "皇家园林", "茶马古道", "丝绸之路", "边塞重镇", "江南水乡", "道教名山", "佛教圣地",
                    "古墓秘境", "江湖门派", "武林盟会", "皇家宝库", "神秘禁区", "世外桃源", "隐世门派", "江湖秘境"
                ],
                "蒸汽朋克": [
                    "齿轮与蒸汽之城", "飞艇交通枢纽", "工业革命中心", "发条机械之都", "黄铜管道网络", "维多利亚风格建筑区", "烟雾缭绕的工厂区", "蒸汽动力车站",
                    "机械生物研究所", "蒸汽朋克博物馆", "齿轮工坊", "蒸汽动力工厂", "机械生物栖息地", "蒸汽朋克集市", "齿轮竞技场", "蒸汽朋克实验室",
                    "机械生物保护区", "蒸汽朋克城堡", "齿轮要塞", "蒸汽朋克港口", "机械生物农场", "蒸汽朋克研究所", "齿轮工坊", "蒸汽朋克医院"
                ],
                "赛博朋克": [
                    "霓虹灯照耀的街道", "数据流交汇处", "黑客活动中心", "企业权力象征", "社会底层聚集地", "悬浮建筑群", "地下反抗军基地", "虚拟现实空间",
                    "义体改造诊所", "记忆存储库", "基因编辑黑市", "纳米机器人工厂", "神经连接中心", "赛博朋克酒吧", "广告墙覆盖区", "数据流黑市",
                    "赛博格竞技场", "网络安全中心", "虚拟现实工厂", "赛博朋克教堂", "神经科学研究所", "人工智能墓地", "量子计算中心", "赛博朋克贫民窟"
                ]
            }
        }
        
        # 视觉元素
        self.images = {}
        self.load_images()
        
        # 当前显示的详细信息索引
        self.current_detail_index = 0
        
        # 创建界面
        self.create_ui()
    
    def setup_styles(self):
        """设置界面样式"""
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except:
            pass
        
        # 配置字体
        default_font = ('SimHei',) if os.name == 'nt' else ('WenQuanYi Micro Hei',)
        self.style.configure('.', background='#f0f0f0', font=default_font)
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        self.style.configure('TButton')
        self.style.configure('Header.TLabel', font=(*default_font, 16, 'bold'))
        self.style.configure('Result.TLabel', font=(*default_font, 14), foreground='#2c3e50')
        self.style.configure('Meaning.TLabel', font=(*default_font, 10), foreground='#7f8c8d')
        
        # 标签页样式
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TNotebook.Tab', padding=[10, 5])
    
    def load_images(self):
        """加载视觉元素图片"""
        try:
            # 尝试加载背景图片
            if os.path.exists("background.jpg"):
                bg_image = Image.open("background.jpg")
                bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
                self.images['background'] = ImageTk.PhotoImage(bg_image)
            
            # 加载风格图标
            styles = ['奇幻', '科幻', '古风', '蒸汽朋克', '赛博朋克']
            for style in styles:
                if os.path.exists(f"{style}.png"):
                    img = Image.open(f"{style}.png")
                    img = img.resize((32, 32), Image.Resampling.LANCZOS)
                    self.images[style] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"加载图片资源时出错: {e}")
    
    def create_ui(self):
        """创建用户界面"""
        # 主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        # 如果有背景图片，添加背景
        if 'background' in self.images:
            bg_label = tk.Label(self.main_frame, image=self.images['background'])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 顶部标题
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(pady=20)
        
        self.header_label = ttk.Label(
            self.header_frame, 
            text="高级世界观生成器", 
            style='Header.TLabel'
        )
        self.header_label.pack()
        
        # 使用标签页组织功能
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 创建生成标签页
        self.create_generation_tab()
        
        # 创建历史记录标签页
        self.create_history_tab()
        
        # 创建收藏夹标签页
        self.create_favorites_tab()
        
        # 底部状态栏
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief='sunken', 
            anchor='w'
        )
        self.status_bar.pack(fill='x', padx=5, pady=5)
        self.update_status("就绪")
    
    def create_generation_tab(self):
        """创建生成标签页"""
        gen_frame = ttk.Frame(self.notebook)
        self.notebook.add(gen_frame, text='生成器')
        
        # 生成选项区域
        options_frame = ttk.Frame(gen_frame)
        options_frame.pack(pady=10, fill='x')
        
        # 类型选择
        type_label = ttk.Label(options_frame, text="选择类型:")
        type_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        self.type_var = tk.StringVar(value='人名')
        self.type_combobox = ttk.Combobox(
            options_frame, 
            textvariable=self.type_var, 
            values=['人名', '地名'], 
            state='readonly', 
            width=15
        )
        self.type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # 风格选择
        style_label = ttk.Label(options_frame, text="选择风格:")
        style_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        
        self.style_var = tk.StringVar(value='奇幻')
        self.style_combobox = ttk.Combobox(
            options_frame, 
            textvariable=self.style_var, 
            values=list(self.styles['人名'].keys()),  # 初始使用人名风格
            state='readonly', 
            width=15
        )
        self.style_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # 绑定类型变化事件，更新风格选项
        self.type_var.trace_add('write', self.update_style_options)
        
        # 批量生成输入框
        batch_label = ttk.Label(options_frame, text="批量生成数量:")
        batch_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.batch_var = tk.StringVar(value='1')
        self.batch_entry = ttk.Entry(options_frame, textvariable=self.batch_var, width=5)
        self.batch_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # 生成按钮
        button_frame = ttk.Frame(options_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        generate_button = ttk.Button(
            button_frame, 
            text='生成名称', 
            command=self.generate_name
        )
        generate_button.pack(side='left', padx=5)
        
        favorite_button = ttk.Button(
            button_frame, 
            text='添加到收藏', 
            command=self.add_to_favorites
        )
        favorite_button.pack(side='left', padx=5)
        
        # 结果显示区域
        result_frame = ttk.Frame(gen_frame)
        result_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 风格图片标签
        self.image_label = tk.Label(result_frame)
        self.image_label.pack()
        
        # 使用文本框替代标签来显示多个结果
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            width=40,
            height=3,
            font=('SimHei', 14)
        )
        self.result_text.pack(pady=10, fill='x')
        self.result_text.config(state='disabled')
        
        # 含义列表
        self.meaning_frame = ttk.Frame(result_frame)
        self.meaning_frame.pack(pady=10, fill='x')
        
        # 详细信息区域
        detail_label = ttk.Label(result_frame, text="详细信息:")
        detail_label.pack(pady=(20, 5))
        
        # 详细信息文本框
        self.detail_text = scrolledtext.ScrolledText(
            result_frame, 
            width=60, 
            height=8
        )
        self.detail_text.pack(fill='both', expand=True)
        
        # 详细信息导航按钮
        self.detail_nav_frame = ttk.Frame(result_frame)
        self.detail_nav_frame.pack(pady=5, fill='x')
        
        self.prev_button = ttk.Button(
            self.detail_nav_frame,
            text="上一个",
            command=self.prev_detail,
            state=tk.DISABLED
        )
        self.prev_button.pack(side='left', padx=5)
        
        self.detail_info_var = tk.StringVar(value="1/1")
        self.detail_info_label = ttk.Label(
            self.detail_nav_frame,
            textvariable=self.detail_info_var
        )
        self.detail_info_label.pack(side='left', padx=10)
        
        self.next_button = ttk.Button(
            self.detail_nav_frame,
            text="下一个",
            command=self.next_detail,
            state=tk.DISABLED
        )
        self.next_button.pack(side='left', padx=5)
    
    def create_history_tab(self):
        """创建历史记录标签页"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text='历史记录')
        
        # 顶部按钮
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(pady=5, fill='x')
        
        clear_history_button = ttk.Button(
            button_frame, 
            text='清空历史记录', 
            command=self.clear_history
        )
        clear_history_button.pack(side='left', padx=5)
        
        # 搜索框
        search_frame = ttk.Frame(history_frame)
        search_frame.pack(pady=5, fill='x')
        search_label = ttk.Label(search_frame, text="搜索:")
        search_label.pack(side='left', padx=5)
        self.history_search_var = tk.StringVar()
        self.history_search_entry = ttk.Entry(search_frame, textvariable=self.history_search_var)
        self.history_search_entry.pack(side='left', fill='x', expand=True, padx=5)
        search_button = ttk.Button(search_frame, text="搜索", command=self.search_history)
        search_button.pack(side='left', padx=5)
        
        # 历史记录列表
        columns = ('时间', '类型', '风格', '名称', '含义')
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # 设置列
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100, anchor='center')
        
        self.history_tree.column('含义', width=200)
        self.history_tree.column('名称', width=150)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(
            history_frame, 
            orient='vertical', 
            command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 双击查看详情
        self.history_tree.bind('<Double-1>', self.view_history_detail)
        
        # 右键菜单
        self.history_menu = tk.Menu(self.root, tearoff=0)
        self.history_menu.add_command(
            label="添加到收藏", 
            command=self.add_history_to_favorites
        )
        self.history_menu.add_command(
            label="删除记录", 
            command=self.delete_history
        )
        self.history_tree.bind('<Button-3>', self.show_history_menu)
        
        # 刷新历史记录
        self.refresh_history()
    
    def create_favorites_tab(self):
        """创建收藏夹标签页"""
        fav_frame = ttk.Frame(self.notebook)
        self.notebook.add(fav_frame, text='我的收藏')
        
        # 顶部按钮
        button_frame = ttk.Frame(fav_frame)
        button_frame.pack(pady=5, fill='x')
        
        clear_favorites_button = ttk.Button(
            button_frame, 
            text='清空收藏夹', 
            command=self.clear_favorites
        )
        clear_favorites_button.pack(side='left', padx=5)
        
        # 搜索框
        search_frame = ttk.Frame(fav_frame)
        search_frame.pack(pady=5, fill='x')
        search_label = ttk.Label(search_frame, text="搜索:")
        search_label.pack(side='left', padx=5)
        self.favorites_search_var = tk.StringVar()
        self.favorites_search_entry = ttk.Entry(search_frame, textvariable=self.favorites_search_var)
        self.favorites_search_entry.pack(side='left', fill='x', expand=True, padx=5)
        search_button = ttk.Button(search_frame, text="搜索", command=self.search_favorites)
        search_button.pack(side='left', padx=5)
        
        # 收藏列表
        columns = ('时间', '类型', '风格', '名称', '含义')
        self.favorites_tree = ttk.Treeview(
            fav_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # 设置列
        for col in columns:
            self.favorites_tree.heading(col, text=col)
            self.favorites_tree.column(col, width=100, anchor='center')
        
        self.favorites_tree.column('含义', width=200)
        self.favorites_tree.column('名称', width=150)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(
            fav_frame, 
            orient='vertical', 
            command=self.favorites_tree.yview
        )
        self.favorites_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.favorites_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 双击查看详情
        self.favorites_tree.bind('<Double-1>', self.view_favorite_detail)
        
        # 右键菜单
        self.favorites_menu = tk.Menu(self.root, tearoff=0)
        self.favorites_menu.add_command(
            label="查看详情", 
            command=self.view_favorite_detail
        )
        self.favorites_menu.add_command(
            label="移除收藏", 
            command=self.remove_favorite
        )
        self.favorites_tree.bind('<Button-3>', self.show_favorites_menu)
        
        # 刷新收藏夹
        self.refresh_favorites()
    
    def update_style_options(self, *args):
        """更新风格选项"""
        current_type = self.type_var.get()
        styles = list(self.styles[current_type].keys())
        self.style_combobox['values'] = styles
        self.style_var.set(styles[0])
    
    def generate_name(self):
        """生成随机名称"""
        try:
            batch_count = int(self.batch_var.get())
            if batch_count <= 0:
                messagebox.showerror("错误", "批量生成数量必须为正整数")
                return
        except ValueError:
            messagebox.showerror("错误", "批量生成数量必须为正整数")
            return
        
        name_type = self.type_var.get()
        style = self.style_var.get()
        
        # 获取当前风格的名称列表
        name_pool = self.styles[name_type][style].copy()
        
        # 检查是否有足够的名称
        if batch_count > len(name_pool):
            messagebox.showwarning("警告", f"该风格下只有 {len(name_pool)} 个不同的名称，将生成全部可用名称。")
            batch_count = len(name_pool)
        
        # 清空结果文本框
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', 'end')
        
        # 清空含义区域
        for widget in self.meaning_frame.winfo_children():
            widget.destroy()
        
        self.current_names = []
        self.current_details = []
        
        for i in range(batch_count):
            try:
                # 随机选择一个名称并从池中移除，确保不重复
                name = random.choice(name_pool)
                name_pool.remove(name)
                
                meaning = random.choice(self.meanings[name_type][style])
                
                # 显示结果
                self.current_names.append(name)
                self.result_text.insert('end', f"{name}\n")
                
                # 生成详细信息
                detail = self.generate_detail(name_type, style, name, meaning)
                self.current_details.append(detail)
                
                # 添加到历史记录
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.history.append({
                    'timestamp': timestamp,
                    'type': name_type,
                    'style': style,
                    'name': name,
                    'meaning': meaning,
                    'detail': detail
                })
                
                # 创建含义标签
                meaning_label = ttk.Label(
                    self.meaning_frame,
                    text=f"{name}: {meaning}",
                    font=('SimHei', 10),
                    foreground='#7f8c8d'
                )
                meaning_label.pack(anchor='w', pady=2)
                
            except Exception as e:
                messagebox.showerror("错误", f"生成名称时出错: {str(e)}")
                self.update_status("生成失败")
                return
        
        # 更新详细信息显示
        self.current_detail_index = 0
        self.update_detail_display()
        
        # 显示风格图片
        if style in self.images:
            self.image_label.config(image=self.images[style])
        else:
            self.image_label.config(image='')
        
        self.refresh_history()
        self.save_data()
        self.update_status(f"成功生成 {batch_count} 个 {name_type} - {style} 风格的名称")
    
    def update_detail_display(self):
        """更新详细信息显示"""
        if not self.current_details:
            self.detail_text.delete('1.0', 'end')
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.detail_info_var.set("0/0")
            return
        
        # 更新详细信息文本
        self.detail_text.delete('1.0', 'end')
        self.detail_text.insert('1.0', self.current_details[self.current_detail_index])
        
        # 更新导航按钮状态
        total = len(self.current_details)
        self.detail_info_var.set(f"{self.current_detail_index + 1}/{total}")
        
        if total == 1:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL if self.current_detail_index > 0 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.current_detail_index < total - 1 else tk.DISABLED)
    
    def prev_detail(self):
        """显示上一个详细信息"""
        if self.current_detail_index > 0:
            self.current_detail_index -= 1
            self.update_detail_display()
    
    def next_detail(self):
        """显示下一个详细信息"""
        if self.current_detail_index < len(self.current_details) - 1:
            self.current_detail_index += 1
            self.update_detail_display()
    
    def generate_detail(self, name_type, style, name, meaning):
        """生成详细信息"""
        if name_type == "人名":
            return f"""名称: {name}
风格: {style}
含义: {meaning}

背景故事:
{name}是一位{random.choice(['著名的', '神秘的', '年轻的', '年长的'])}{meaning}。
{random.choice(['他', '她'])}来自{random.choice(['一个贵族家庭', '偏远山村', '神秘组织', '流浪民族'])},
以{random.choice(['勇敢', '智慧', '狡诈', '忠诚'])}著称。"""

        else:  # 地名
            return f"""名称: {name}
风格: {style}
含义: {meaning}

地点描述:
{name}是一个{random.choice(['繁华的', '荒凉的', '神秘的', '危险的'])}{meaning}。
这里以{random.choice(['独特的建筑', '奇异的风俗', '丰富的资源', '战略位置'])}闻名，
{random.choice(['吸引着众多游客', '被当地人视为圣地', '是兵家必争之地', '隐藏着不为人知的秘密'])}。"""
    
    def add_to_favorites(self):
        """添加当前生成结果到收藏夹"""
        if not self.current_names:
            messagebox.showwarning("警告", "没有可收藏的生成结果")
            return
        
        added_count = 0
        
        for name in self.current_names:
            # 在历史记录中查找匹配项
            for record in reversed(self.history):
                if record['name'] == name:
                    # 检查是否已经收藏
                    if any(fav['name'] == name and fav['meaning'] == record['meaning'] for fav in self.favorites):
                        continue
                    
                    # 添加到收藏夹
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.favorites.append({
                        'timestamp': timestamp,
                        'type': record['type'],
                        'style': record['style'],
                        'name': record['name'],
                        'meaning': record['meaning'],
                        'detail': record['detail']
                    })
                    added_count += 1
                    break
        
        if added_count > 0:
            self.refresh_favorites()
            self.save_data()
            self.update_status(f"已收藏 {added_count} 个名称")
    
    def add_history_to_favorites(self):
        """将选中的历史记录添加到收藏夹"""
        selected_items = self.history_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要收藏的记录")
            return
        
        added_count = 0
        for item_id in selected_items:
            item = self.history_tree.item(item_id)
            values = item['values']
            
            # 查找历史记录中的对应项
            for record in self.history:
                if (record['timestamp'] == values[0] and 
                    record['type'] == values[1] and 
                    record['name'] == values[3]):
                    
                    # 检查是否已经收藏
                    if any(fav['name'] == record['name'] and fav['meaning'] == record['meaning'] for fav in self.favorites):
                        continue
                    
                    # 添加到收藏夹
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.favorites.append({
                        'timestamp': timestamp,
                        'type': record['type'],
                        'style': record['style'],
                        'name': record['name'],
                        'meaning': record['meaning'],
                        'detail': record['detail']
                    })
                    added_count += 1
                    break
        
        if added_count > 0:
            self.refresh_favorites()
            self.save_data()
            self.update_status(f"已收藏 {added_count} 个名称")
        else:
            messagebox.showinfo("提示", "所选记录已全部收藏")
    
    def view_history_detail(self, event=None):
        """查看历史记录详情"""
        selected_item = self.history_tree.selection()
        if not selected_item:
            return
        
        item = self.history_tree.item(selected_item[0])
        values = item['values']
        
        # 查找历史记录中的对应项
        for record in self.history:
            if (record['timestamp'] == values[0] and 
                record['type'] == values[1] and 
                record['name'] == values[3]):
                
                # 更新当前显示的详细信息
                self.current_names = [record['name']]
                self.current_details = [record['detail']]
                self.current_detail_index = 0
                self.update_detail_display()
                
                # 切换到生成器标签页
                self.notebook.select(0)
                
                break
    
    def view_favorite_detail(self, event=None):
        """查看收藏详情"""
        selected_item = self.favorites_tree.selection()
        if not selected_item:
            return
        
        item = self.favorites_tree.item(selected_item[0])
        values = item['values']
        
        # 查找收藏中的对应项
        for record in self.favorites:
            if (record['timestamp'] == values[0] and 
                record['type'] == values[1] and 
                record['name'] == values[3]):
                
                # 更新当前显示的详细信息
                self.current_names = [record['name']]
                self.current_details = [record['detail']]
                self.current_detail_index = 0
                self.update_detail_display()
                
                # 切换到生成器标签页
                self.notebook.select(0)
                
                break
    
    def delete_history(self):
        """删除选中的历史记录"""
        selected_items = self.history_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的记录")
            return
        
        # 确认删除
        if messagebox.askyesno("确认", "确定要删除选中的历史记录吗？"):
            deleted_count = 0
            for item_id in selected_items:
                item = self.history_tree.item(item_id)
                values = item['values']
                
                # 从历史记录中删除
                self.history = [record for record in self.history if not (
                    record['timestamp'] == values[0] and 
                    record['type'] == values[1] and 
                    record['name'] == values[3]
                )]
                deleted_count += 1
            
            # 刷新历史记录
            self.refresh_history()
            self.save_data()
            self.update_status(f"已删除 {deleted_count} 条历史记录")
    
    def remove_favorite(self):
        """移除选中的收藏"""
        selected_items = self.favorites_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要移除的收藏")
            return
        
        # 确认移除
        if messagebox.askyesno("确认", "确定要移除选中的收藏吗？"):
            removed_count = 0
            for item_id in selected_items:
                item = self.favorites_tree.item(item_id)
                values = item['values']
                
                # 从收藏中删除
                self.favorites = [record for record in self.favorites if not (
                    record['timestamp'] == values[0] and 
                    record['type'] == values[1] and 
                    record['name'] == values[3]
                )]
                removed_count += 1
            
            # 刷新收藏夹
            self.refresh_favorites()
            self.save_data()
            self.update_status(f"已移除 {removed_count} 条收藏")
    
    def clear_history(self):
        """清空历史记录"""
        if messagebox.askyesno("确认", "确定要清空所有历史记录吗？"):
            self.history = []
            self.refresh_history()
            self.save_data()
            self.update_status("已清空所有历史记录")
    
    def clear_favorites(self):
        """清空收藏夹"""
        if messagebox.askyesno("确认", "确定要清空所有收藏吗？"):
            self.favorites = []
            self.refresh_favorites()
            self.save_data()
            self.update_status("已清空所有收藏")
    
    def search_history(self):
        """搜索历史记录"""
        search_text = self.history_search_var.get().strip().lower()
        if not search_text:
            self.refresh_history()
            return
        
        # 筛选匹配的历史记录
        filtered_history = []
        for record in self.history:
            if (search_text in record['name'].lower() or 
                search_text in record['meaning'].lower() or 
                search_text in record['type'].lower() or 
                search_text in record['style'].lower()):
                filtered_history.append(record)
        
        # 显示筛选结果
        self.refresh_history(filtered_history)
    
    def search_favorites(self):
        """搜索收藏夹"""
        search_text = self.favorites_search_var.get().strip().lower()
        if not search_text:
            self.refresh_favorites()
            return
        
        # 筛选匹配的收藏
        filtered_favorites = []
        for record in self.favorites:
            if (search_text in record['name'].lower() or 
                search_text in record['meaning'].lower() or 
                search_text in record['type'].lower() or 
                search_text in record['style'].lower()):
                filtered_favorites.append(record)
        
        # 显示筛选结果
        self.refresh_favorites(filtered_favorites)
    
    def refresh_history(self, history_list=None):
        """刷新历史记录列表"""
        # 清空当前显示
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # 使用指定的历史列表或全部历史
        history_to_display = history_list or self.history
        
        # 添加历史记录到列表
        for record in history_to_display:
            self.history_tree.insert(
                '', 
                'end', 
                values=(
                    record['timestamp'], 
                    record['type'], 
                    record['style'], 
                    record['name'], 
                    record['meaning']
                )
            )
    
    def refresh_favorites(self, favorites_list=None):
        """刷新收藏夹列表"""
        # 清空当前显示
        for item in self.favorites_tree.get_children():
            self.favorites_tree.delete(item)
        
        # 使用指定的收藏列表或全部收藏
        favorites_to_display = favorites_list or self.favorites
        
        # 添加收藏到列表
        for record in favorites_to_display:
            self.favorites_tree.insert(
                '', 
                'end', 
                values=(
                    record['timestamp'], 
                    record['type'], 
                    record['style'], 
                    record['name'], 
                    record['meaning']
                )
            )
    
    def show_history_menu(self, event):
        """显示历史记录右键菜单"""
        region = self.history_tree.identify_region(event.x, event.y)
        if region == "cell":
            self.history_tree.selection_set(self.history_tree.identify_row(event.y))
            self.history_menu.post(event.x_root, event.y_root)
    
    def show_favorites_menu(self, event):
        """显示收藏夹右键菜单"""
        region = self.favorites_tree.identify_region(event.x, event.y)
        if region == "cell":
            self.favorites_tree.selection_set(self.favorites_tree.identify_row(event.y))
            self.favorites_menu.post(event.x_root, event.y_root)
    
    def load_data(self):
        """加载保存的数据"""
        try:
            if os.path.exists("world_generator_data.json"):
                with open("world_generator_data.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    
                    # 加载历史记录
                    if 'history' in data:
                        self.history = data['history']
                    
                    # 加载收藏夹
                    if 'favorites' in data:
                        self.favorites = data['favorites']
        except Exception as e:
            print(f"加载数据时出错: {e}")
    
    def save_data(self):
        """保存数据"""
        try:
            data = {
                'history': self.history,
                'favorites': self.favorites
            }
            
            with open("world_generator_data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存数据时出错: {e}")
    
    def update_status(self, message):
        """更新状态栏消息"""
        self.status_var.set(message)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedWorldGenerator(root)
    root.mainloop() 