import networkx as nx
import matplotlib.pyplot as plt
import japanize_matplotlib


def draw_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)

    # Specify the edges you want here
    # edge_colors = ['black' for edge in G.edges()]
    black_edges = [edge for edge in G.edges()]

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    pos = nx.spring_layout(G, k=1.0)
    colors = ["red","green","yellow","blue","magenta"]
    node_sizes = [1200,1200,1200,1200,1200]
    edge_labels = {("明治", "大正"):"親子", ("大正", "昭和"):"師弟", ("昭和", "平成"):"仲間", ("平成", "令和"):"家族", ("昭和", "明治"):"メンバー"}
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('Reds'), \
        node_color = colors, node_size=node_sizes)
    nx.draw_networkx_edges(G, pos, edge_color=["red", "green", "yellow", "blue", "magenta"], edgelist=black_edges, width=[k["weight"] for i, j, k in G.edges(data=True)])
    nx.draw_networkx_labels(G,pos,font_family='IPAexGothic')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color='red', font_family='IPAexGothic', rotate="False")
    plt.axis('off')
    plt.show()

edges = [('明治','大正', {"weight":5}),('大正','昭和', {"weight":12}),('昭和','平成', {"weight":7}), \
        ('平成','令和', {"weight":3}),('昭和','明治', {"weight":6})]
draw_graph(edges)