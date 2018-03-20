import networkx as nx
import plotly as py
import plotly.graph_objs as go
import os
import pickle


def Unpickle_Dic():
    master_dic = pickle.load(
        open(os.path.join(os.getcwd(), "Requisites/referenceDic.p"), mode="rb"))
    for key, val in list(master_dic.items()):
        try:
            del master_dic[key][key[2:4]]
        except KeyError:
            pass
    return master_dic


def Find_Distinct_Nodes(master_dic):
    nodelist = []
    for key, val in master_dic.items():
        if key[2:4] not in nodelist:
            nodelist.append(key[2:4])
        for key2 in val.keys():
            if key2 not in nodelist:
                nodelist.append(key2)
    return nodelist


def Count_References(nodelist, master_dic):
    nodedict = {key: {"In": {}, "Out": {}, "InC": 0, "OutC": 0}
                for key in nodelist}
    for key, val in master_dic.items():
        nodedict[key[2:4]]["Out"] = val
        for key2, val2 in val.items():
            nodedict[key2]["In"][key] = val2
    for node in nodelist:
        nodedict[node]["InC"] = sum(nodedict[node]["In"].values())
        nodedict[node]["OutC"] = sum(nodedict[node]["Out"].values())

    return nodedict


def Create_Graph(master_dic):
    G = nx.DiGraph()
    nodelist = Find_Distinct_Nodes(master_dic)
    nodedict = Count_References(nodelist, master_dic)
    for each in nodelist:
        G.add_node(each, key=each)
    for key3, val3 in master_dic.items():
        for key2, val2 in val3.items():
            G.add_edge(key3[2:4], key2, no_of_references=val2)

    pos = nx.spring_layout(G)
    for key2, val2 in pos.items():
        G.add_node(key2, key=key2, pos=val2, text="NP{0}".format(key2))

    Draw_Graph(G, nodedict)


def Draw_Graph(G, nodedict):
    pos = nx.get_node_attributes(G, 'pos')
    dmin = 1
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5)**2 + (y - 0.5)**2
        if d < dmin:
            dmin = d

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=go.Line(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    external_annotations = []
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

        # Adds the arrows
        '''external_annotations.append(dict(
            ax = x0,
            ay = y0,
            axref = 'x',
            ayref = 'y',
            x = x1,
            y = y1,
            xref = 'x',
            yref = 'y',
            showarrow = True,
            standoff = 2,
            arrowhead = 3,
            arrowsize = 1,
            arrowwidth = 1.5,
            arrowcolor = '#636363'
        ))'''
    # Adds final external_annotations
    external_annotations.append(dict(
        showarrow=False,
        xref="paper", yref="paper",
        x=0.005, y=-0.002))

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=go.Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='Picnic',
            reversescale=True,
            color=[],
            opacity=1,
            size=10,
            symbol="circle",
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2, color='#000000')))

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    node_trace['marker']['size'] = []
    for node, adjacencies in G.adjacency():
        node_trace['marker']['size'].append(10 + len(nodedict[node]["In"]) * 5)
        node_trace['marker']['color'].append(nodedict[node]["InC"])
        node_info = '<b>NP{0}</b><br>In: {1}<br>Out: {2}<br>Individual Refernces: {3}'.format(
            node, len(nodedict[node]["In"]), len(nodedict[node]["Out"]), nodedict[node]["InC"])
        node_trace['text'].append(node_info)

    fig = go.Figure(data=go.Data([edge_trace, node_trace]),
                    layout=go.Layout(
        title='<br>UKHO References Network Graph',
        titlefont=dict(size=16),
        showlegend=False,
        # font=dict(family='Arial'),
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        annotations=external_annotations,
        xaxis=go.XAxis(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=go.YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    py.offline.plot(fig, filename='networkx')


if __name__ == "__main__":
    master_dic = Unpickle_Dic()
    Capital_GEEEE = Create_Graph(master_dic)
