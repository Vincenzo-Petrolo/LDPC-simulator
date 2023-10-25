from tanner import Tanner
import utilities as u
import channel as c
import codeword_gen as codegen
import numpy as np
import matplotlib.pyplot as plt
import tqdm


if __name__ == "__main__":

    vns = 6
    cns = 3

    T = Tanner(vns, cns, adjmatr_file="h2.txt")
    # Generate new random message and let it through a noisy channel using BPSK modulation
    codeword = codegen.Code("h2.txt").codeword()
    print(f"Sent codeword: {codeword}")
    channel_LLRs = c.erasure_channel(u.BPSK(codeword), snr=1.5)
    print(f"Received codeword: {u.LLR2Binary(channel_LLRs)}")
    # Decode the received mssage
    decoded = T.decode(channel_LLRs, max_iterations=200, visual=True)
    print(f"Decoded codeword: {decoded}")