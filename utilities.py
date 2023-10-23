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
        if (c == 1):
            bpsk.append(-1)
        else:
            bpsk.append(1)
    
    return bpsk
