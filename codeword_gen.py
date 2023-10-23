import numpy as np
import random

class Code(object):
    def __init__(self, adjmatr_file) -> None:
        self.H = np.loadtxt(adjmatr_file, dtype=int)
        self.G = np.hstack([ np.eye(3),self.H[:,:3]])
    
    def codeword(self) -> list:
        seed = [random.choice([0,1]) for _ in range(3)]
        
        return (seed @ self.G) % 2