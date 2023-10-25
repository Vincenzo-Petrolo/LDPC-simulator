import random


def LLR2Binary(LLRs : list) -> list:
    msg = []

    for llr in LLRs:
        if (llr < -0.2):
            msg.append("1")
        elif (llr > 0.2):
            msg.append("0")
        else:
            msg.append("?")

    return msg

def BPSK(codeword : list) -> list:
    bpsk = []

    for c in codeword:
        noise = abs(random.gauss(mu=0, sigma=0.1))

        # print(f"Injecting noise {noise}")

        if (c == 1):
            bpsk.append(-1 + noise)
        else:
            bpsk.append(1 + noise)
    
    return bpsk
