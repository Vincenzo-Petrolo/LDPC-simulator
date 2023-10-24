from tanner import Tanner
import random
import utilities as u
import channel as c
import codeword_gen as codegen
import numpy as np
import matplotlib.pyplot as plt
import tqdm


if __name__ == "__main__":

    vns = 6
    cns = 3
    n_txs = 100
    max_SNR_per_bit = 1.3 # dB (Higher is better)
    samples = 1000
    decoding_iteration = 100

    T = Tanner(vns, cns, adjmatr_file="ldpc_adjmatr.txt")

    # Sweep on an uniform SNR
    SNRs = np.linspace(1, max_SNR_per_bit, num=samples)
    BERs = []
    bar = tqdm.tqdm(total=samples)

    for snr in SNRs:
        # Store number of wrong bits after each transmission
        wrong_bits = []

        for _ in range(n_txs):
            # Generate new random message and let it through a noisy channel using BPSK modulation
            codeword = codegen.Code("ldpc_adjmatr.txt").codeword()
            channel_LLRs = c.erasure_channel(u.BPSK(codeword), snr)
            # Decode the received mssage
            errors = "".join(T.decode(channel_LLRs, max_iterations=decoding_iteration, visual=False)).count("?")
            wrong_bits.append(errors)

        bar.update()
        avg_ber = np.average(wrong_bits)
        bar.write(f"Simulating {snr : .3f} SNR | Avg. BER: {avg_ber}")
        
        BERs.append(avg_ber)
    
    plt.figure(figsize=(8, 6))
    plt.semilogy(SNRs, BERs, label="BER")
    plt.xlabel('Eb/No')
    plt.ylabel('BER')
    plt.ylim(10e-15, 1)
    plt.xlim(1, max_SNR_per_bit)
    plt.grid(True)
    plt.legend()
    plt.show()