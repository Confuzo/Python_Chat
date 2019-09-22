# Diffie-Hellman
import random

class DiffieHellman():
    def __init__(self, q, alpha):
        self.q = q
        self.alpha = alpha

    def calculate_pubkey(self):
        self.x = random.randrange(0, self.q)
        self.y = (self.alpha ** self.x) % self.q
        return self.y
    
    def calculate_sessionkey(self, foreign_key):
        self.k = (foreign_key ** self.x) % self.q
        return self.k
