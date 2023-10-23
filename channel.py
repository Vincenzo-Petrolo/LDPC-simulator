import random

def flip_channel(msg : list, ber : float) -> list:
    out_msg = []

    for i in range(len(msg)):
        if (random.uniform(0,1) <= ber):
            out_msg.append(msg[i]*-1)
        else:
            out_msg.append(msg[i])

    return out_msg

def erasure_channel(msg : list, ber : float) -> list:
    out_msg = []

    for i in range(len(msg)):
        if (random.uniform(0,1) <= ber):
            out_msg.append(0)
        else:
            out_msg.append(msg[i])

    return out_msg