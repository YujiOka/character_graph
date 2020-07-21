import networkx as nx
import matplotlib.pyplot as plt
import japanize_matplotlib

# 文章を走査
def calc_sent(G, text):
    return G

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
    G = calc_sent(G, text)

    # G.add_edges_from(edges)
    # pos = nx.spring_layout(G)
    # plt.figure()
    # labels = {"A":"岡","B":"浜","C":"池","D":"中"}
    # nx.draw(G,pos,edge_color='black',width=1,linewidths=1,\
    # node_size=500,node_color='pink',alpha=0.9)
    # nx.draw_networkx_labels(G, pos, labels=labels, font_family="IPAexGothic")
    # nx.draw_networkx_edge_labels(G,pos,edge_labels={('A','B'):'友達',\
    # ('B','C'):'友達',('B','D'):'敵'},font_color='red', font_family='IPAexGothic')

    # edges = [('明治','大正', {"weight":5}),('大正','昭和', {"weight":12}),('昭和','平成', {"weight":7}), \
    #     ('平成','令和', {"weight":3}),('昭和','明治', {"weight":6})]
    # pos = nx.spring_layout(G, k=1.0)
    # colors = ["red","green","yellow","blue","magenta"]
    # node_sizes = [1200,1200,1200,1200,1200]
    # edge_labels = {("明治", "大正"):"親子", ("大正", "昭和"):"師弟", ("昭和", "平成"):"仲間", ("平成", "令和"):"家族", ("昭和", "明治"):"メンバー"}
    # nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('Reds'), \
    #     node_color = colors, node_size=node_sizes)
    # nx.draw_networkx_edges(G, pos, edge_color=["red", "green", "yellow", "blue", "magenta"], edgelist=black_edges, width=[k["weight"] for i, j, k in G.edges(data=True)])
    # nx.draw_networkx_labels(G,pos,font_family='IPAexGothic')
    # nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color='red', font_family='IPAexGothic', rotate="False")

    # plt.axis('off')
    # plt.show()

if __name__ == "__main__":
    make_graph()