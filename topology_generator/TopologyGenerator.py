import networkx as nx
import json
import random
from math import ceil

class TopologyGenerator:

    def generate_topology(iot_nodes, YAFS_sim, levels, fog0_reduction_factor, edge_prob_0, fogi_reduction_factor, hub_prob):
        """
            iot_nodes: number of nodes
            YAFS_sim: if True iot_nodes are replaced with gateawys, for the use with YAFS
            levels: number of levels
            fog0_reduction_factor: reduction factor for FOG 0 Level (starting from iot_nodes)
            edge_prob_0: probability of edge generation in the fog level 0 (range: [0, 1], suggested: 0.01)
            fogi_reduction_factor: reduciton factor for FOG >0 levels (starting from the number of nodes of FOG 0 level)
            hub_prob: the higher this value the higher the amount of hubs with high degree (range: [0, 1])
        """
        G = nx.Graph() # Main Graph
        H = nx.Graph() # Helper graph, used for generating sub-graph for each level

        ranges = [] # {"nodes": label of nodes for each level, "highest_degrees": 20% of nodes with higher degrees}

        # IoT devices and FOG/Cloud levels generation
        for level in range(levels):
            if level == 0:
                # IoT nodes generated as "stand-alone" nodes without interconnection (sensors and actuators)
                # this level is generated only if YAFS_sim is False
                if not YAFS_sim:
                    H = nx.Graph()
                    #H.add_nodes_from([(i, {"class[z]": level}) for i in range(iot_nodes)]) # [z] is used for Gephi visualization with the Network Splitter 3D layout
                    H.add_nodes_from([(i, {"level": "iot"}) for i in range(iot_nodes)])

            elif level == 1:
                # FOG-0 level generation: "private" fog nodes
                H = nx.Graph()
                if not YAFS_sim:
                    H = nx.gnp_random_graph(iot_nodes // fog0_reduction_factor, edge_prob_0)
                else:
                    #H.add_nodes_from([(i, {"class[z]": level}) for i in range(iot_nodes // 5)]) # [z] is used for Gephi visualization with the Network Splitter 3D layout
                    H.add_nodes_from([(i, {"level": "gateway"}) for i in range(iot_nodes // 5)])
            elif level == levels-1:
                H = nx.Graph()
                #H.add_nodes_from([(0, {"class[z]": level})])
                H.add_nodes_from([(0, {"level": "cloud"})]) # CLOUD

            else:
                # FOG level > 0
                new_nodes = iot_nodes // (fogi_reduction_factor ** (level-1)) if iot_nodes // (fogi_reduction_factor**(level-1)) >= 2 else 2
                
                # Small-World graph generation for FOG levels greater than 0 (e.g provincial fog nodes)
                H = nx.watts_strogatz_graph(int(new_nodes), 2, hub_prob)
                nx.set_node_attributes(H, level-2, "level")
                
            # Remapping nodes label
            mapping = dict(zip(H, range(len(G.nodes), len(G.nodes) + len(H.nodes))))
            H = nx.relabel_nodes(H, mapping)
            nx.set_node_attributes(H, level, "class[z]")

            # Selection of the 20% of nodes with highest degree
            highest_degrees = [n[0] for n in sorted(H.degree, key=lambda x: x[1], reverse=True)[:ceil((len(H.nodes)/100)*20)]]

            ranges.append({"nodes": list(H.nodes), "highest_degrees": highest_degrees})
            
            # Append the generated graph to the Main Graph
            G = nx.compose(G, H)

        # Connection between levels
        for level in range(levels-1):
            
            connection_to_upper_level = 0 # counter of connection to upper levels

            for node_from in ranges[level]["nodes"]:

                # only 20% of node in fog levels > 1 are connected to upper levels
                if level > 1 and random.randrange(100) > 20:
                    # If there aren't connection to upper levels a link is generated
                    if node_from == ranges[level]["nodes"][-1:] and connection_to_upper_level == 0:
                        G.add_edge(node_from, random.choice(ranges[level+1]["highest_degrees"]))
                    
                    continue

                connection_to_upper_level += 1
            
                ## there's a 5 % chance that nodes are connected to non-touching upper levels
                for r in range(random.randrange(1, levels-1)):
                    rnd_level_to = level+1
                    while random.randrange(100) < 20:
                        rnd_level_to += 1
                        if(rnd_level_to >= levels):
                            rnd_level_to = level+1
                            break
                
                    G.add_edge(node_from, random.choice(ranges[rnd_level_to]["highest_degrees" if level > 0 else "nodes"]))

        return G


def main():
    G = TopologyGenerator.generate_topology(iot_nodes=2000, 
                                            YAFS_sim=True, 
                                            levels=5, 
                                            fog0_reduction_factor=50, 
                                            edge_prob_0=0, 
                                            fogi_reduction_factor=3/2, 
                                            hub_prob=0.1)
    nx.write_gexf(G, "test.gexf")

if __name__ == '__main__':
    main()
