import random
import math

def SNR2ber(snr : float):
    # Higher SNR -> extremely low bit error rate
    return math.exp(-2*(snr-1))

def flip_channel(msg : list, snr : float) -> list:
    out_msg = []

    ber = SNR2ber(snr)

    for i in range(len(msg)):
        if (random.uniform(0,1) <= ber):
            out_msg.append(msg[i]*-1)
        else:
            out_msg.append(msg[i])

    return out_msg

def erasure_channel(msg : list, snr : float) -> list:
    out_msg = []

    ber = SNR2ber(snr)

    for i in range(len(msg)):
        if (random.uniform(0,1) <= ber):
            out_msg.append(random.choice([-0.1, 0.1]))
        else:
            out_msg.append(msg[i])

    return out_msg