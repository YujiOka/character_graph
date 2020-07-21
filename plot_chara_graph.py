import networkx as nx
import matplotlib.pyplot as plt
import japanize_matplotlib

# キャラをGに代入
def add_chara(G, chara):
    for c in chara:
        G.add_node(c[0], weight=c[1], color=c[2])

# 既存のエッジを収集
def existing_connect(G):
    tmp = []
    for i, j, k in G.edges(data=True):
        tmp.append([i,j,k])
    return tmp

# 既存のエッジの中に文中に出てきたキャラの関係があるかチェック
def connect_check(c_1, c_2, connect):
    for con in connect:
        if (con[0] == c_1 or con[0] == c_2) and (con[1] == c_1 or con[1] == c_2):
            return con[2]["weight"]
    return 0

# 関係表現からの距離を算出
def calc_distance(pos, distance, start_dis, end_dis):
    for i in range(len(distance)):
        if end_dis < distance[i]:
            distance[i] = (distance[i] - pos) * 1.3
        elif start_dis > distance[i]:
            distance[i] = (pos - distance[i]) * 1.3
        elif distance[i] > pos:
            distance[i] = distance[i] - pos
        else:
            distance[i] = pos - distance[i]

# 関係表現の宛先を決定
def calc_rel(pos, candidate, distance, start_dis, end_dis):
    tmp1 = 0
    tmp2 = 1
    calc_distance(pos, distance, start_dis, end_dis)
    for i in range(2, len(distance)):
        if distance[tmp2] > distance[i]:
            tmp2 = i
    for j in range(1, len(distance)):
        if distance[tmp1] > distance[j] and candidate[tmp2] != candidate[j]:
            tmp1 = j
    return candidate[tmp1], candidate[tmp2]

# 関係表現を全て抽出
def get_relation_name(text, rel_position):
    num = rel_position + 1
    name = text[rel_position][0]
    while text[num][1][-2].replace("B-", "").replace("I-", "") == "REL":
        name += text[num][0]
        num += 1
    return name

# 関係表現からエッジのラベルを命名
def detect_relation(text, rel_position):
    tmp = text[rel_position][0]
    if tmp in ["祖父", "祖母", "親", "母", "父", "兄", "弟", "姉", "妹",  "息子", "娘", "いとこ", "おじ", "おば", "孫", "嫁", "妻", "夫", "甥", "姪"]:
        return "家族"
    elif tmp in ["上司", "部下"]:
        return "上司・部下"
    elif tmp in ["師匠", "弟子"]:
        return "師弟"
    elif tmp in ["先生", "生徒"]:
        return "先生・生徒"
    return get_relation_name(text, rel_position)

# 関係表現周辺の人物とその位置を抽出
def search_distance(text, pos, candidate, distance, after_flag, start_dis, end_dis):
    for i in range(len(text)):
        if i < pos and text[i][0] in ["。", "」"]:
            start_dis = i
        if i > pos and text[i][0] in ["。", "」"] and not after_flag:
                end_dis = i
                after_flag = True
                continue
        if text[i][1][-1] != "O":
            candidate.append(text[i][1][-1])
            distance.append(i)
        if after_flag and text[i][0] in ["。", "」"]:
            break
    return start_dis, end_dis

# 関係表現に最も近い二人のキャラのエッジにラベル付け
def add_rel_to_edge(G, text, rel_position):
    candidate = [] # 関係表現の宛先候補
    distance = [] # 関係表現からの距離
    after_flag = False
    start_dis = -1
    end_dis = -1
    for pos in rel_position:
        start_dis, end_dis = search_distance(text, pos, candidate, distance, after_flag, start_dis, end_dis)
        rel = detect_relation(text, pos)
        can_1, can_2 = calc_rel(pos, candidate, distance, start_dis, end_dis)
        G.add_edge(can_1, can_2, label=rel)
        candidate = []
        distance = []
    

# 文章に出てきたキャラを関連付け
def connect_chara(t_chara, G, rel_position, text):
    e_cnct = existing_connect(G)
    for i in range(len(t_chara)):
        for j in range(i+1, len(t_chara)):
            w_num = connect_check(t_chara[i], t_chara[j], e_cnct)
            if w_num == 0:
                G.add_edge(t_chara[i], t_chara[j], weight=1, label="")
            else:
                G.add_edge(t_chara[i], t_chara[j], weight=w_num+1)
    if rel_position[0] != -1:
        add_rel_to_edge(G, text, rel_position)

# 関係表現が出てきた位置を記憶
def remember_relation(rel_position, text, t):
    if rel_position[0] == -1:
        rel_position[0] = text.index(t)
    else:
        rel_position.append(text.index(t))

# 二次元配列charaのインデックスを検索
def search_chara(chara, text):
    for i in range(len(chara)):
        if chara[i][0] == text:
            break
    return i

# 性別によってノードの色を変化
def calc_sex(text, chara):
    if text[0] in ["彼"]:
        chara[search_chara(chara, text[1][-1])][2] = "blue"
    elif text[0] in ["彼女"]:
        chara[search_chara(chara, text[1][-1])][2] = "red"

# キャラを計数
def calc_chara(chara, t_chara, text):
    name = [c[0] for c in chara]
    if text[1][-1] not in name:
        chara.append([text[1][-1], 1, "green"])  # 名前、weight、名前の色（性別）
    else:
        chara[search_chara(chara, text[1][-1])][1] += 1
    if text[1][-2].replace("B-","") != "NAME":
        calc_sex(text, chara)
    if text[1][-1] not in t_chara:
        t_chara.append(text[1][-1])

# 文章に出てきた人物を格納
def end_sent(G, t_chara, rel_position, text):
    if t_chara != []:
        connect_chara(t_chara, G, rel_position, text)

# 文章を走査
def calc_sent(G, text):
    chara = []  # 全体のキャラ
    t_chara = []  # 一文中のキャラ
    rel_position = [-1]  # 関係表現の出現位置
    for t in text:
        if t[0] in ["。", "」"]:
            end_sent(G, t_chara, rel_position, text)
            t_chara = []
            rel_position = [-1]
        elif t[1][-1] != "O":
            calc_chara(chara, t_chara, t)
        elif t[1][-2].replace("B-","") == "REL":
            remember_relation(rel_position, text, t)
    add_chara(G, chara)

# ファイルから教師テキスト読み出し
def open_file(file_name):
    with open(file_name, mode="r") as f:
        lines = f.read()
    morphs = lines.split("\n")
    while morphs[-1] == "":
        morphs.pop(-1)
    morphs = [morph.split("\t") for morph in morphs]
    for i in range(len(morphs)):
        morphs[i][1] = morphs[i][1].split(",")
    return morphs

# グラフ作成プログラム本体
def make_graph():
    G = nx.Graph()
    text = open_file("data/tmp.txt")
    calc_sent(G, text)

    pos = nx.spring_layout(G)
    plt.figure()
    # print(G.edges(data=True))
    # labels = {("ゴーシュ", "アレン"):"仕事仲間"}
    # print(labels)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('Reds'), node_color=[j["color"] for i, j in G.nodes(data=True)] ,alpha=0.5, node_size=[j["weight"]*1500 for i, j in G.nodes(data=True)])
    nx.draw_networkx_edges(G, pos, edge_color="black", width=[k["weight"] for i, j, k in G.edges(data=True)])
    nx.draw_networkx_labels(G,pos,font_family='IPAexGothic')
    nx.draw_networkx_edge_labels(G,pos,edge_labels={(i, j):k["label"] for i, j, k in G.edges(data=True)},font_color='red', font_family='IPAexGothic', rotate="False")
    # print(G.nodes(data=True))
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    make_graph()