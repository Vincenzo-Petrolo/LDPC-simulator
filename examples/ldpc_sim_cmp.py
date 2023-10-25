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
    n_txs = 1000
    max_SNR_per_bit = 5
    samples = 100
    decoding_iteration = 50

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
            codeword1 = codegen.Code("h1.txt").codeword()
            channel_LLRs1 = c.erasure_channel(u.BPSK(codeword1), snr)
            codeword2 = codegen.Code("h2.txt").codeword()
            channel_LLRs2 = c.erasure_channel(u.BPSK(codeword2), snr)
            codeword3 = codegen.Code("h3.txt").codeword()
            channel_LLRs3 = c.erasure_channel(u.BPSK(codeword3), snr)
            codeword4 = codegen.Code("h4.txt").codeword()
            channel_LLRs4 = c.erasure_channel(u.BPSK(codeword4), snr)
            # Decode the received mssage
            decoded1 = "".join(T1.decode(channel_LLRs1, max_iterations=decoding_iteration, visual=False))
            decoded2 = "".join(T2.decode(channel_LLRs2, max_iterations=decoding_iteration, visual=False))
            decoded3 = "".join(T3.decode(channel_LLRs3, max_iterations=decoding_iteration, visual=False))
            decoded4 = "".join(T4.decode(channel_LLRs4, max_iterations=decoding_iteration, visual=False))
            original1 = "".join([str(int(c)) for c in codeword1])
            original2 = "".join([str(int(c)) for c in codeword2])
            original3 = "".join([str(int(c)) for c in codeword3])
            original4 = "".join([str(int(c)) for c in codeword4])

            errors = count_bit_differences(decoded1, original1)
            wrong_bits1.append(errors)
            errors = count_bit_differences(decoded2, original2)
            wrong_bits2.append(errors)
            errors = count_bit_differences(decoded3, original3)
            wrong_bits3.append(errors)
            errors = count_bit_differences(decoded4, original4)
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