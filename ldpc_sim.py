from tanner import Tanner
import random
import utilities as u
import channel as c
import codeword_gen as codegen


if __name__ == "__main__":

    vns = 6
    cns = 3

    channel_LLRs = c.erasure_channel(u.BPSK(codegen.Code("ldpc_adjmatr.txt").codeword()), ber=0.1)

    print(f"Received message: {u.LLR2Binary(channel_LLRs)}")

    T = Tanner(vns, cns, adjmatr_file="ldpc_adjmatr.txt")
    decoded_msg = T.decode(channel_LLRs, max_iterations=200)

    print(f"Decoded message: {decoded_msg}")