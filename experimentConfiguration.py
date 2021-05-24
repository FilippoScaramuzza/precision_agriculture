from topology_generator.TopologyGenerator import TopologyGenerator
import json
import random

class ExperimentConfiguration:

    def __init__(self):
        self.IOT_DEVICES_NUM = 2000
        self.NETWORK_LEVELS_NUM = 5
        self.REDUCTION_FACTOR_1 = 50 # IOT -> FOG-0 nodes reduction factor
        self.LINK_GENERATION_PROBABILITY_FOG0 = 0.01
        self.REDUCTION_FACTOR_2 = 2 # FOG-i -> FOG-i+1 nodes reduction factor
        self.HUB_GENERATION_PROBABILITY = 0.1

        self.FUNC_NODE_RAM_IOT = "'{:.6f}'.format(random.randrange(1, 10) * 10**-6)"
        self.FUNC_NODE_RAM_FOG0 = "'{:.6f}'.format(random.randrange(1, 10) * 10**-2)"
        self.FUNC_NODE_RAM_FOG1 = "'{:.6f}'.format(random.randrange(1, 10) * 10**-1)"
        self.FUNC_NODE_RAM_FOG2 = "'{:.6f}'.format(random.randrange(1, 10) * 10**-1)"
        self.FUNC_NODE_RAM_CLOUD = "9999999999999999"

        self.FUNC_NODE_IPT_IOT = "'{:.6f}'.format(random.randrange(1, 10) * 10**-2)"
        self.FUNC_NODE_IPT_FOG0 = "'{:.6f}'.format(random.randrange(1, 10) * 10**-1)"
        self.FUNC_NODE_IPT_FOG1 = "'{:.6f}'.format(random.randrange(1, 10) * 10**0)"
        self.FUNC_NODE_IPT_FOG2 = "'{:.6f}'.format(random.randrange(1, 10) * 10)"
        self.FUNC_NODE_IPT_CLOUD = "9999"

        self.FUNC_EDGE_PR_SAME_LEVEL = "random.randrange(1, 10)"
        self.FUNC_EDGE_BW_SAME_LEVEL = "random.randrange(20, 30)"
        self.FUNC_EDGE_PR_ADJ_LEVEL = "random.randrange(20, 30)"
        self.FUNC_EDGE_BW_ADJ_LEVEL = "random.randrange(5, 10)"
        self.FUNC_EDGE_PR_NON_ADJ_LEVEL = "random.randrange(30, 40)"
        self.FUNC_EDGE_BW_NON_ADJ_LEVEL = "random.randrange(1, 5)"

    def userGeneration(self):
        # TODO
        return

    def appGeneration(self):
        # TODO
        return

    def networkGeneration(self):
        #**************************************
        #generation of the network topology
        #**************************************

        # TOPOLOGY GENERATION

        network_graph = TopologyGenerator.generate_topology(self.IOT_DEVICES_NUM,
                                          self.NETWORK_LEVELS_NUM,
                                          self.REDUCTION_FACTOR_1,
                                          self.LINK_GENERATION_PROBABILITY_FOG0,
                                          self.REDUCTION_FACTOR_2,
                                          self.HUB_GENERATION_PROBABILITY)

        for i in range(len(network_graph.nodes)):
            if network_graph.nodes[i]["class[z]"] == 0:
                network_graph.nodes[i]["RAM"] = eval(self.FUNC_NODE_RAM_IOT)
                network_graph.nodes[i]["IPT"] = eval(self.FUNC_NODE_IPT_IOT)
            elif network_graph.nodes[i]["class[z]"] == 1:
                network_graph.nodes[i]["RAM"] = eval(self.FUNC_NODE_RAM_FOG0)
                network_graph.nodes[i]["IPT"] = eval(self.FUNC_NODE_IPT_FOG0)
            elif network_graph.nodes[i]["class[z]"] == 2:
                network_graph.nodes[i]["RAM"] = eval(self.FUNC_NODE_RAM_FOG1)
                network_graph.nodes[i]["IPT"] = eval(self.FUNC_NODE_IPT_FOG1)
            elif network_graph.nodes[i]["class[z]"] == 3:
                network_graph.nodes[i]["RAM"] = eval(self.FUNC_NODE_RAM_FOG2)
                network_graph.nodes[i]["IPT"] = eval(self.FUNC_NODE_IPT_FOG2)
            elif network_graph.nodes[i]["class[z]"] == 4:
                network_graph.nodes[i]["RAM"] = eval(self.FUNC_NODE_RAM_CLOUD)
                network_graph.nodes[i]["IPT"] = eval(self.FUNC_NODE_IPT_CLOUD)

        for u, v in network_graph.edges:
            if network_graph.nodes[u]["class[z]"] == network_graph.nodes[v]["class[z]"]:
                network_graph[u][v]["PR"] = eval(self.FUNC_EDGE_PR_SAME_LEVEL)
                network_graph[u][v]["BW"] = eval(self.FUNC_EDGE_BW_SAME_LEVEL)

            elif abs(int(network_graph.nodes[u]["class[z]"]) - int(network_graph.nodes[v]["class[z]"])):
                network_graph[u][v]["PR"] = eval(self.FUNC_EDGE_PR_ADJ_LEVEL)
                network_graph[u][v]["BW"] = eval(self.FUNC_EDGE_BW_ADJ_LEVEL)
            else:
                network_graph[u][v]["PR"] = eval(self.FUNC_EDGE_PR_ADJ_LEVEL)
                network_graph[u][v]["BW"] = eval(self.FUNC_EDGE_BW_ADJ_LEVEL)

        json.dump(dict(entity=[dict(id=n, 
                                    RAM=network_graph.nodes[n]["RAM"], 
                                    IPT=network_graph.nodes[n]["IPT"]) for n in network_graph.nodes()],
                       link=[dict(s=u, 
                                  d=v, 
                                  PR=network_graph[u][v]["PR"],
                                  BW=network_graph[u][v]["BW"]) for u,v in network_graph.edges()]),
        open("topologyDefinition.json", 'w'), indent=2)

        return 

    def loadConfiguration(self):
        # TODO
        return 

if __name__ == "__main__":
    EC = ExperimentConfiguration()
    EC.networkGeneration()
