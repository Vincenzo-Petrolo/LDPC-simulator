import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from nodes import VariableNode, CheckNode
from matplotlib.animation import FuncAnimation
import utilities as u
import numpy as np


class Tanner(object):

    def __init__(self, vns, cns, adjmatr_file=None, number_edges = None):
        if adjmatr_file:
            # Load the adjacency matrix from the file
            adjacency_matrix = np.loadtxt(adjmatr_file, dtype=int)
            # Create a bipartite graph from the adjacency matrix
            self.T = nx.Graph()

            self.T.add_nodes_from(range(vns), bipartite=0)  # VNS
            self.T.add_nodes_from(range(vns, vns + cns), bipartite=1)  # CNS

            for i in range(cns):
                for j in range(vns):
                    if adjacency_matrix[i, j] == 1:
                        self.T.add_edge(i + vns, j)
        else:
            self.T = bipartite.gnmk_random_graph(vns, cns, number_edges)

        self.vns = vns
        self.cns = cns

        # Create memory matrix to exchange messages
        self.vns2cns = np.zeros(adjacency_matrix.shape)
        self.cns2vns = np.zeros(adjacency_matrix.shape)

        vns = list(self.T.nodes)[:self.vns]
        cns = list(self.T.nodes)[self.vns:]

        # Set up all the Variable nodes
        for vn in vns:
            nx.set_node_attributes(self.T, values={vn: {"obj": VariableNode(node_id=vn)}})

        # Set up all the Check nodes
        for cn in cns:
            nx.set_node_attributes(self.T, values={cn: {"obj": CheckNode()}})
 
    def show(self, iteration):
        plt.cla()
        # Plot the bipartite graph
        vns = list(self.T.nodes)[:self.vns]
        cns = list(self.T.nodes)[self.vns:]

        pos = nx.bipartite_layout(self.T, vns)

        # Draw edges
        nx.draw(self.T, pos, with_labels=False, node_size=500, font_size=10)

        # Draw variable nodes with labels including LLR values
        LLRs = [self.T.nodes[vn]["obj"].getLLR(self.cns2vns) for vn in vns]
        messages = u.LLR2Binary(LLRs)

        vns_labels = {i : f'{LLRs[i] : .1f} {msg}' for i, msg in enumerate(messages)}
        nx.draw_networkx_labels(self.T, pos, labels=vns_labels, font_size=12)

        vns_node_colors = []

        for i in range(len(messages)):
            if (messages[i] == "?"):
                vns_node_colors.append("#ea5146")
            elif (messages[i] == "0"):
                vns_node_colors.append("#7ec174")
            else:
                vns_node_colors.append("#7499c1")

        # Parity check colors
        cns_node_colors = []
        
        for cn in range(self.vns, self.cns + self.vns):
            if (self.parityCheck(cn)):
                cns_node_colors.append("g")
            else:
                cns_node_colors.append("r")

        # Draw custom node shapes
        nx.draw_networkx_nodes(self.T, pos, nodelist=cns, node_shape='s', node_color=cns_node_colors, node_size=500)
        nx.draw_networkx_nodes(self.T, pos, nodelist=vns, node_shape='o', node_color=vns_node_colors, node_size=500)

        # Add a title with the current iteration
        title = f'Iteration: {iteration + 1}'
        plt.title(title, fontsize=12)


    def simulate(self, initial_LLRs : list, max_iterations : int) -> None:
        # Create the figure
        fig, ax = plt.subplots()

        def update(iteration):
            if (self.checkDone()):
                return

            # First phase: Update VNS
            self.updateVNS(initial_LLRs)
            # Second phase: Update CNS
            self.updateCNS()
            
            self.show(iteration)

        anim = FuncAnimation(fig, func=update, frames=max_iterations, repeat=False, init_func=None)
        plt.show()

        return
    
    def getNeighboorsMessages(self, node_id) -> dict:
        neighboors = list(self.T.neighbors(node_id))
        messages = {}

        if (node_id < self.vns):
            # Gather messages from check nodes
            for n in neighboors:
                messages[n-self.vns] = self.cns2vns[n-self.vns][node_id]
        else:
            for n in neighboors:
                messages[n] = self.vns2cns[node_id - self.vns][n]

        return messages

    def updateVNS(self, channel_LLRs : list = None):
        vns = list(self.T.nodes)[:self.vns]
        nodes = self.T.nodes(data=True)

        for i, vn in enumerate(vns):
            cns_messages = self.getNeighboorsMessages(vn)
            out_msgs = nodes[vn]["obj"].compute_message(channel_LLRs[i], cns_messages)

            for node, out_msg in out_msgs.items():
                self.vns2cns[node][i] = out_msg

        return

    def updateCNS(self):
        cns = list(self.T.nodes)[self.vns:]
        nodes = self.T.nodes(data=True)

        for i, cn in enumerate(cns):
            vns_messages = self.getNeighboorsMessages(cn)
            out_msgs = nodes[cn]["obj"].compute_message(vns_messages)

            for node, out_msg in out_msgs.items():
                self.cns2vns[i][node] = out_msg

        return
    
    def checkDone(self) -> bool:
        for cn in range(self.vns, self.cns + self.vns):
            if (not self.parityCheck(cn)):
                return False

        return True
    
    def parityCheck(self, cn):
        neighbors = self.T.neighbors(cn)

        LLRs = [self.T.nodes[vn]["obj"].getLLR(self.cns2vns) for vn in neighbors]
        sign = 1

        for llr in LLRs:
            if (llr < -0.1):
                sign *= -1
            
            if (abs(llr) < 0.1):
                return False

        if (sign < 0 or sum(LLRs) == 0):
            return False

        return True
    
    def decode(self, channel_LLRs : list, max_iterations = 100) -> list:
        # First simulate the decoder behavior
        self.channel_LLRs = channel_LLRs
        self.simulate(channel_LLRs, max_iterations)

        # Gather the LLRs
        LLRs = [node[1]["obj"].getLLR(self.cns2vns) for node in list(self.T.nodes(data=True))[:self.vns]]

        decoded_msg = u.LLR2Binary(LLRs)

        return decoded_msg

