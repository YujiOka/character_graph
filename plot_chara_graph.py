import networkx as nx
import matplotlib.pyplot as plt
import japanize_matplotlib


edges=[['A','B'],['B','C'],['B','D']]
G=nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)
plt.figure()
labels = {"A":"岡","B":"浜","C":"池","D":"中"}
nx.draw(G,pos,edge_color='black',width=1,linewidths=1,\
node_size=500,node_color='pink',alpha=0.9)
nx.draw_networkx_labels(G, pos, labels=labels, font_family="IPAexGothic")
nx.draw_networkx_edge_labels(G,pos,edge_labels={('A','B'):'友達',\
('B','C'):'友達',('B','D'):'敵'},font_color='red', font_family='IPAexGothic')
plt.axis('off')
plt.show()