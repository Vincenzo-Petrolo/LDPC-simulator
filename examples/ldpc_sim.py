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
    max_SNR_per_bit = 2
    samples = 100
    decoding_iteration = 10

    T = Tanner(vns, cns, adjmatr_file="h1.txt")

    # Sweep on an uniform SNR
    SNRs = np.linspace(1, max_SNR_per_bit, num=samples)
    BERs = []
    bar = tqdm.tqdm(total=samples)

    for snr in SNRs:
        # Store number of wrong bits after each transmission
        wrong_bits = []

        for _ in range(n_txs):
            # Generate new random message and let it through a noisy channel using BPSK modulation
            codeword = codegen.Code("h1.txt").codeword()
            channel_LLRs = c.erasure_channel(u.BPSK(codeword), snr)
            # Decode the received mssage
            decoded = "".join(T.decode(channel_LLRs, max_iterations=decoding_iteration, visual=False))
            original = "".join([str(int(c)) for c in codeword])
            errors = count_bit_differences(decoded, original)
            wrong_bits.append(errors)

        bar.update()
        avg_ber = np.average(wrong_bits)
        bar.write(f"Simulating {snr : .3f} SNR | Avg. BER: {avg_ber}")
        
        BERs.append(avg_ber)
    
    plt.figure(figsize=(6, 4))
    plt.semilogy(SNRs, BERs, label="BER")
    plt.xlabel('Eb/No')
    plt.ylabel('BER')
    plt.ylim(10e-15, 10)
    plt.xlim(1, max_SNR_per_bit)
    plt.grid(True)
    plt.legend()
    plt.show()