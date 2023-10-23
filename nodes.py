class VariableNode(object):
    def __init__(self) -> None:
        self.last_message = 0                                                # Last output message
        pass

    def compute_message(self, channel_LLR = None, cn_messages : list = None) -> float:

        # print(f"[Variable Node] Received: {cn_messages}, Channel LLR: {channel_LLR}")
        self.last_message = sum(cn_messages) + float(channel_LLR)
        # print(f"[Variable Node] Computed: {self.last_message:.2f}")

        return self.last_message

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
        self.last_message = 0
        self.alpha = 0.9
        pass

    
    def compute_message(self, vn_messages : list = None) -> float:
        # Uses MinSum algorithm

        # print(f"[Check Node] Received: {vn_messages}")
        self.last_message = self.alpha * sign(vn_messages) * min([abs(llr) for llr in vn_messages])
        # print(f"[Check Node] Computed: {self.last_message:.2f}")

        return self.last_message
