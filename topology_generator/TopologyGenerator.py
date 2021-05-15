import networkx as nx
import json
import random

class TopologyGenerator:
    
    def generate_topology(iot_nodes, levels, k):
        """
            0 - IOT
            1 - FOG 1
            2 - FOG 2
            k - CLOUD
        """
        G = nx.Graph()
        H = nx.Graph()

        for level in range(levels):
            if level == 0:
                H = nx.Graph()
                H.add_nodes_from([(i, {"class[z]": level}) for i in range(iot_nodes)])

            else:
                new_nodes = iot_nodes // (k**level) if iot_nodes // (k**level) >=2 else 2
                H = nx.barabasi_albert_graph(new_nodes, 1)

                mapping = dict(zip(H, range(len(G.nodes), len(G.nodes) + iot_nodes//(k**level))))
                H = nx.relabel_nodes(H, mapping)
                nx.set_node_attributes(H, level, "class[z]")
                
            G = nx.compose(G, H)

        for level in range(levels):
            if level == 0:
                for node_from in [node_from for node_from in G.nodes if node_from < iot_nodes]:
                    
                    rnd_level_to = 1
                    while random.randrange(100) < 20:
                        rnd_level_to += 1
                        if(rnd_level_to > levels):
                            rnd_level_to = 1
                            break

                    to_nodes = iot_nodes
                    for l in range(1, rnd_level_to+1):
                        to_nodes += iot_nodes//(k**l)
                    G.add_edge(node_from, random.choice([node_to for node_to in G.nodes if node_to > iot_nodes and node_to < to_nodes]))
        

        nx.write_gexf(G, "test.gexf")   
        return G


def main():
    G = TopologyGenerator.generate_topology(500, 4, 3)

if __name__ == '__main__':
    main()
    