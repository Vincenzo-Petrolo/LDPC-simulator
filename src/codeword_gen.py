import numpy as np
import random

class Code(object):
    def __init__(self, adjmatr_file) -> None:
        self.H = np.loadtxt(adjmatr_file, dtype=int)
        shape = self.H.shape
        self.G = np.hstack([ np.eye(shape[0]),self.H[:,:shape[1]-shape[0]]])
    
    def codeword(self) -> list:
        shape = self.H.shape
        seed = [random.choice([0,1]) for _ in range(shape[0])]
        
        return (seed @ self.G) % 2