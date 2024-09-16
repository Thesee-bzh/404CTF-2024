from LFSR import LFSR
from generator import CombinerGenerator
from z3 import *

# Define states as lists of BitVec of size 1
# - Lists  because this is used in LFSR
# - BitVec because of the combination
state1 = [BitVec("state1_%i" % i, 1) for i in range(19)]
state2 = [BitVec("state2_%i" % i, 1) for i in range(19)]
state3 = [BitVec("state3_%i" % i, 1) for i in range(19)]

#Polynomial representation
poly1 = [19,5,2,1] # x^19+x^5+x^2+x
poly2 = [19,6,2,1] # x^19+x^6+x^2+x
poly3 = [19,9,8,5] # x^19+x^9+x^8+x^5

#Create LFSRs
L1 = LFSR(fpoly=poly1,state=state1)
L2 = LFSR(fpoly=poly2,state=state2)
L3 = LFSR(fpoly=poly3,state=state3)

# Read files
with open("flag.png.part","rb") as f1: flag_part = f1.read()
with open("flag.png.enc","rb")  as f2: flag_enc = f2.read()

# Recover keystream by xoring partial clear flag with encoded flag
def xor(b1, b2): return bytes(a ^ b for a, b in zip(b1, b2))
keystream = xor(flag_part, flag_enc)

# Turn keystream into bits
outputs = []
for b in keystream: outputs += [int(x) for x in bin(b)[2:].rjust(8, '0') ]

def combine(x1, x2, x3):
    return (x1 * x2)^(x2 * x3)^(x1 * x3)

# Add constraints, solve
s = Solver()
for i in range(len(outputs)):
    s.add(outputs[i] == combine(L1.generateBit(), L2.generateBit(), L3.generateBit()))
assert s.check() == sat

# Recover initial states
m = s.model()
state1 = [m.evaluate(state1[i]) for i in range(19)]
state2 = [m.evaluate(state2[i]) for i in range(19)]
state3 = [m.evaluate(state3[i]) for i in range(19)]
print(f"{state1 = }")
print(f"{state2 = }")
print(f"{state3 = }")
