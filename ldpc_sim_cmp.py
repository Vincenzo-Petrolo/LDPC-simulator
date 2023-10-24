from tanner import Tanner
import random
import utilities as u
import channel as c
import codeword_gen as codegen
import numpy as np
import matplotlib.pyplot as plt
import tqdm


def count_bit_differences(binary_str1, binary_str2):
    if len(binary_str1) != len(binary_str2):
        raise ValueError("Binary strings must have the same length")

    difference_count = 0
    for bit1, bit2 in zip(binary_str1, binary_str2):
        if bit1 != bit2:
            difference_count += 1

    return difference_count

if __name__ == "__main__":

    vns = 6
    cns = 3
    n_txs = 500
    max_SNR_per_bit = 2
    samples = 100
    decoding_iteration = 10

    T1 = Tanner(vns, cns, adjmatr_file="h1.txt")
    T2 = Tanner(vns, cns, adjmatr_file="h2.txt")
    T3 = Tanner(vns, cns, adjmatr_file="h3.txt")
    T4 = Tanner(vns, cns, adjmatr_file="h4.txt")

    # Sweep on an uniform SNR
    SNRs = np.linspace(1, max_SNR_per_bit, num=samples)
    BERs1 = []
    BERs2 = []
    BERs3 = []
    BERs4 = []
    bar = tqdm.tqdm(total=samples)

    for snr in SNRs:
        # Store number of wrong bits after each transmission
        wrong_bits1 = []
        wrong_bits2 = []
        wrong_bits3 = []
        wrong_bits4 = []

        for _ in range(n_txs):
            # Generate new random message and let it through a noisy channel using BPSK modulation
            codeword = codegen.Code("ldpc_adjmatr.txt").codeword()
            channel_LLRs = c.erasure_channel(u.BPSK(codeword), snr)
            # Decode the received mssage
            decoded1 = "".join(T1.decode(channel_LLRs, max_iterations=decoding_iteration, visual=False))
            decoded2 = "".join(T2.decode(channel_LLRs, max_iterations=decoding_iteration, visual=False))
            decoded3 = "".join(T3.decode(channel_LLRs, max_iterations=decoding_iteration, visual=False))
            decoded4 = "".join(T4.decode(channel_LLRs, max_iterations=decoding_iteration, visual=False))
            original = "".join([str(int(c)) for c in codeword])

            errors = count_bit_differences(decoded1, original)
            wrong_bits1.append(errors)
            errors = count_bit_differences(decoded2, original)
            wrong_bits2.append(errors)
            errors = count_bit_differences(decoded3, original)
            wrong_bits3.append(errors)
            errors = count_bit_differences(decoded4, original)
            wrong_bits4.append(errors)

        bar.update()
        
        BERs1.append(np.average(wrong_bits1))
        BERs2.append(np.average(wrong_bits2))
        BERs3.append(np.average(wrong_bits3))
        BERs4.append(np.average(wrong_bits4))
    
    plt.figure(figsize=(6, 4))
    plt.semilogy(SNRs, BERs1, label="H1")
    plt.semilogy(SNRs, BERs2, label="H2")
    plt.semilogy(SNRs, BERs3, label="H3")
    plt.semilogy(SNRs, BERs4, label="H4")
    plt.xlabel('Eb/No')
    plt.ylabel('BER')
    plt.ylim(10e-15, 10)
    plt.xlim(1, max_SNR_per_bit)
    plt.grid(True)
    plt.legend()
    plt.show()