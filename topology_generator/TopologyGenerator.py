import networkx as nx
import json

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

        nx.write_gexf(G, "test.gexf")
        return G


def main():
    G = TopologyGenerator.generate_topology(500, 4, 3)

if __name__ == '__main__':
    main()
    