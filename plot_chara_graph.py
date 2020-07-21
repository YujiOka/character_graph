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

# 関係表現を全て抽出
def get_relation_name(text, rel_position):
    num = rel_position + 1
    name = text[rel_position][0]
    while text[num][1][-2].replace("B-", "").replace("I-", "") == "REL":
        name += text[num][0]
    return name

# 関係表現からエッジのラベルを命名
def detect_relation(text, rel_position):
    tmp = text[rel_position][0]
    if tmp in ["祖父", "祖母", "親", "母", "父", "兄", "弟", "姉", "妹",  "息子", "娘", "いとこ", "おじ", "おば", "孫", "嫁", "妻", "夫", "甥", "姪"]:
        return "家族"
    return get_relation_name(text, rel_position)

# 関係表現に最も近い二人のキャラのエッジにラベル付け
def add_rel_to_edge(G, text, rel_position):
    before_candidate = []  # 関係表現より前のキャラ
    after_candidate = []  # 関係表現より後のキャラ
    for posi in rel_position:
        for i in range(posi):
            if text[i][1][-1] != "O":
                before_candidate.append(text[i][1][-1])
        for i in range(posi+1, len(text)):
            if text[i][1][-1] != "O":
                after_candidate.append(text[i][1][-1])
        rel = detect_relation(text, posi)
        G.add_edge(before_candidate[-1], after_candidate[0], label=rel)
    

# 文章に出てきたキャラを関連付け
def connect_chara(t_chara, G, rel_position, text):
    e_cnct = existing_connect(G)
    for i in range(len(t_chara)):
        for j in range(i+1, len(t_chara)):
            w_num = connect_check(t_chara[i], t_chara[j], e_cnct)
            if w_num == 0:
                G.add_edge(t_chara[i], t_chara[j], weight=1, label="nomal")
            else:
                G.add_edge(t_chara[i], t_chara[j], weight=w_num+1)
    if rel_position[0] != -1:
        add_rel_to_edge(G, text, rel_position)
    # print(G.edges(data=True))

# 関係表現が出てきた位置を記憶
def remember_relation(rel_position, text, t):
    if rel_position[0] == -1:
        rel_position[0] = text.index(t)
    else:
        rel_position.append(text.index(t))

# 性別によってノードの色を変化
def calc_sex(text, chara):
    if text[0] in ["彼"]:
        chara[chara[0].index(text[1][-1])][2] = "blue"
    elif text[0] in ["彼女"]:
        chara[chara[0].index(text[1][-1])][2] = "red"

# キャラを計数
def calc_chara(chara, t_chara, text):
    name = [c[0] for c in chara]
    if text[1][-1] not in name:
        chara.append([text[1][-1], 1, "green"])  # 名前、weight、名前の色（性別）
    else:
        chara[chara[0].index(text[1][-1])][1] += 1
    if text[1][-2].replace("B-","") != "NAME":
        calc_sex(text, chara)
    if text[1][-1] not in t_chara:
        t_chara.append(text[1][-1])

# 文章に出てきた人物を格納
def end_sent(G, t_chara, rel_position, text):
    if t_chara != []:
        connect_chara(t_chara, G, rel_position, text)
    t_chara = []

# 文章を走査
def calc_sent(G, text):
    chara = []  # 全体のキャラ
    t_chara = []  # 一文中のキャラ
    rel_position = [-1]  # 関係表現の出現位置
    for t in text:
        if t[0] == "。":
            end_sent(G, t_chara, rel_position, text)
        elif t[1][-1] != "O":
            calc_chara(chara, t_chara, t)
        elif t[1][-2].replace("B-","") == "REL":
            remember_relation(rel_position, text, t)
    # print(chara)
    add_chara(G, chara)

# ファイルから教師テキスト読み出し
def open_file(file_name):
    with open(file_name, mode="r") as f:
        lines = f.read()
    morphs = lines.split("\n")
    morphs.pop(-1)
    morphs = [morph.split("\t") for morph in morphs]
    for i in range(len(morphs)):
        morphs[i][1] = morphs[i][1].split(",")
    return morphs

# グラフ作成プログラム本体
def make_graph():
    G = nx.Graph()
    text = open_file("data/tmp.txt")
    # G = calc_sent(G, text)
    calc_sent(G, text)

    # G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    plt.figure()
    # labels = {"A":"岡","B":"浜","C":"池","D":"中"}
    # nx.draw(G,pos,edge_color='black',node_size=5,alpha=0.9)
    # nx.draw_networkx_labels(G, pos, labels=labels, font_family="IPAexGothic")
    # nx.draw_networkx_edge_labels(G,pos,edge_labels={('A','B'):'友達',\
    # ('B','C'):'友達',('B','D'):'敵'},font_color='red', font_family='IPAexGothic')

    # edges = [('明治','大正', {"weight":5}),('大正','昭和', {"weight":12}),('昭和','平成', {"weight":7}), \
    #     ('平成','令和', {"weight":3}),('昭和','明治', {"weight":6})]
    # pos = nx.spring_layout(G, k=1.0)
    # colors = ["red","green","yellow","blue","magenta"]
    # node_sizes = [1200,1200,1200,1200,1200]
    # edge_labels = {("明治", "大正"):"親子", ("大正", "昭和"):"師弟", ("昭和", "平成"):"仲間", ("平成", "令和"):"家族", ("昭和", "明治"):"メンバー"}
    print(G.edges(data=True))
    # labels = {("ゴーシュ", "アレン"):"仕事仲間"}
    # print(labels)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('Reds'), node_color=[j["color"] for i, j in G.nodes(data=True)] ,alpha=0.5, node_size=[j["weight"]*100 for i, j in G.nodes(data=True)])
    # nx.draw_networkx_edges(G, pos, edge_color="black", edgelist=black_edges, width=[k["weight"] for i, j, k in G.edges(data=True)])
    nx.draw_networkx_edges(G, pos, edge_color="black", width=[k["weight"] for i, j, k in G.edges(data=True)])
    nx.draw_networkx_labels(G,pos,font_family='IPAexGothic')
    nx.draw_networkx_edge_labels(G,pos,edge_labels={(i, j):k["label"] for i, j, k in G.edges(data=True)},font_color='red', font_family='IPAexGothic', rotate="False")
    
    # print(G.nodes(data=True))
    
    

    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    make_graph()