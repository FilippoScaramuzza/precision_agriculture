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

        ranges = []

        # IoT devices and FOG/Cloud levels generation
        for level in range(levels):
            if level == 0:
                H = nx.Graph()
                H.add_nodes_from([(i, {"class[z]": level})
                                 for i in range(iot_nodes)])

            else:
                new_nodes = iot_nodes // (k **
                                          level) if iot_nodes // (k**level) >= 2 else 2
                H = nx.barabasi_albert_graph(new_nodes, 1)

                mapping = dict(
                    zip(H, range(len(G.nodes), len(G.nodes) + iot_nodes//(k**level))))
                H = nx.relabel_nodes(H, mapping)
                nx.set_node_attributes(H, level, "class[z]")

            ranges.append({"from": len(G.nodes), "to": len(G.nodes) + len(H.nodes) - 1})
            G = nx.compose(G, H)

        # Connection between levels
        for level in range(levels-1):
            
            for node_from in [node_from for node_from in G.nodes if node_from >= ranges[level]["from"] and node_from < ranges[level]["to"]]:

                # only 20% of node in fog levels are connected to upper levels
                if level > 0 and random.randrange(100) > 20:
                    continue
                
                rnd_level_to = level+1
                while random.randrange(100) < 20:
                    rnd_level_to += 1
                    if(rnd_level_to >= levels):
                        rnd_level_to = level+1
                        break

                G.add_edge(node_from, random.choice(
                    [node_to for node_to in G.nodes if node_to >= ranges[rnd_level_to]["from"] and node_to <= ranges[rnd_level_to]["to"]]))

        nx.write_gexf(G, "test.gexf")
        return G


def main():
    G = TopologyGenerator.generate_topology(500, 4, 5)


if __name__ == '__main__':
    main()
