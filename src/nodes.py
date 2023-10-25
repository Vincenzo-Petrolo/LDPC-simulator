class VariableNode(object):
    def __init__(self, node_id) -> None:
        self.channel_LLR = 0
        self.node_id = node_id
        pass

    def compute_message(self, channel_LLR = None, cn_messages : dict = None) -> dict:
        out_messages = {}
        # For each check node compute the extrinsic information
        for node, inmsg in cn_messages.items():
            # Compute extrinsic information (subtract incoming message)
            out_messages[node] = sum(list(cn_messages.values())) + float(channel_LLR) - inmsg 

        return out_messages
    
    def getLLR(self, last_messages : dict, channelLLR) -> float:
        return sum(last_messages[:, self.node_id]) + channelLLR 

def sign(vn_messages : list):
    # Initialize a count variable for negative numbers
    count = 0

    # Count the negative numbers in the list
    for llr in vn_messages:
        if llr < 0:
            count += 1

    # Check if the count is even or odd
    if count % 2 == 0:
        return 1  # Return 1 if count is even
    else:
        return -1  # Return -1 if count is odd

class CheckNode(object):
    def __init__(self) -> None:
        self.alpha = 0.75
        pass

    
    def compute_message(self, vn_messages : dict = None) -> dict:
        # Uses MinSum algorithm
        out_messages = {}
        # Compute extrinsic information for each connected variable node
        for node, item in vn_messages.items():
            out_messages[node] = self.alpha * sign([value for key,value in vn_messages.items() if (key != node)]) * min([abs(llr) for key, llr in vn_messages.items() if (key != node)])

        return out_messages 