<div style="text-align: justify">

# Topology Generator

The class ```TopologyGenerator``` is a tool for generating layared networks (```networkx``` graphs) for simulating Fog Computing realistic scenarios.

## How to use and how it works

### How to use
To generate a graph the ```generate_topology``` method is required:
```python
generate_topology(iot_nodes, levels, k1, p1, k2, p2)
```
Where:
- ```iot_nodes``` is the amount of IoT-level nodes (sensors and actuators). There isn't the need to specify the amount of nodes for the upper levels since they are computed from the amount of IoT nodes. (see ```k``` below).
 - ```levels``` is the amount of levels for the layered topology.
 - The Fog Level 0 (e.g. private nodes) has ```1/k1``` of ```iot_nodes```.
 - ```p1``` is the probability of edge generation in the fog level 0 (range: [0, 1], suggested: 0.01)
 - Fog Levels greater than 0, have ```1/k2``` of the nodes of the previous level.
 - ```p2```: the higher this value the higher the amount of hubs with high degree (range: [0, 1])

**Example**
```python
from TopologyGenerator import TopologyGenerator

G = TopologyGenerator.generate_topology(2000, 5, 50, 0.01, 2, 0.1)
```
 
 ### How it works

Nodes in their belonging level (exluding the IoT level) are interconnected using a specific criterion, following the *small-world network* model (<a href="https://en.wikipedia.org/wiki/Small-world_network">Small-world Network</a>). In particular in this generator is used the ```watts_strogatz_graph``` method from ```networkx```. This method returns a random graph according to the Watts–Strogatz model (<a href="https://en.wikipedia.org/wiki/Watts%E2%80%93Strogatz_model">Wikipedia</a>) preferential attachment model.

The nodes in the IoT layer are not connected to each other, since it is rare that sensors and attuctors are connected. 

For Fog Levels 1 and above, the 20% of the nodes in level ```i``` have a 80% chance to be connected to a random node chosen from the 20% of the nodes with the highest degree of the level ```i + 1```. Nodes that not satisfy this percentage have a 80% chance to be connected to a random node in the level ```i + 2```, and so on.
