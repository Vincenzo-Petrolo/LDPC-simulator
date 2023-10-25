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

    vns1 = 6
    cns1 = 3
    vns2 = 8
    cns2 = 4
    n_txs = 500
    max_SNR_per_bit = 5
    samples = 100
    decoding_iteration = 10

    T1 = Tanner(vns1, cns1, adjmatr_file="h1.txt")
    T2 = Tanner(vns2, cns2, adjmatr_file="h1_8,4.txt")

    # Sweep on an uniform SNR
    SNRs = np.linspace(1, max_SNR_per_bit, num=samples)
    BERs1 = []
    BERs2 = []
    bar = tqdm.tqdm(total=samples)

    for snr in SNRs:
        # Store number of wrong bits after each transmission
        wrong_bits1 = []
        wrong_bits2 = []

        for _ in range(n_txs):
            # Generate new random message and let it through a noisy channel using BPSK modulation
            codeword1 = codegen.Code("h1.txt").codeword()
            codeword2 = codegen.Code("h1_8,4.txt").codeword()
            channel_LLRs1 = c.erasure_channel(u.BPSK(codeword1), snr)
            channel_LLRs2 = c.erasure_channel(u.BPSK(codeword2), snr)
            # Decode the received mssage
            decoded1 = "".join(T1.decode(channel_LLRs1, max_iterations=decoding_iteration, visual=False))
            decoded2 = "".join(T2.decode(channel_LLRs2, max_iterations=decoding_iteration, visual=False))
            original1 = "".join([str(int(c)) for c in codeword1])
            original2 = "".join([str(int(c)) for c in codeword2])

            errors = count_bit_differences(decoded1, original1)
            wrong_bits1.append(errors)
            errors = count_bit_differences(decoded2, original2)
            wrong_bits2.append(errors)
        bar.update()
        
        BERs1.append(np.average(wrong_bits1))
        BERs2.append(np.average(wrong_bits2))
    
    plt.figure(figsize=(6, 4))
    plt.semilogy(SNRs, BERs1, label="H1 (6,3)")
    plt.semilogy(SNRs, BERs2, label="H2 (8,4)")
    plt.xlabel('Eb/No')
    plt.ylabel('BER')
    plt.ylim(10e-15, 10)
    plt.xlim(1, max_SNR_per_bit)
    plt.grid(True)
    plt.legend()
    plt.show()