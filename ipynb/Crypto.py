# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#P1 Encryption/Decryption
from binascii import *        #Hex conversion
from collections import deque #Queue
from string import Template   #Output formatting
import re

class Cipher:
    def __init__(self):
        pass
    def enc(self):
        print "No Encryption Algorithm Added"
    def dec(self):
        print "No Encryption Algorithm Added"
class Caesar(Cipher):
    def __init__(self):
        pass
    def enc(self):
        print "UnCaesar"
        

# <codecell>

TEST = Caesar()
TEST.dec()
TEST.enc()
Blah=unhexlify(hexlify("Test"))
"Test"

# <codecell>

#(Extended) Euclid Algorithm
#
def Euclid(a,b,pt=0):
    Temp=Euc([1,0,a],[0,1,b],[[['A1','A2','A3'],['B1','B2','B3']]])
    T=Temp[0]
    print '\n({0})({1})+({2})({3})={4}'.format(a,T[0],b,T[1],T[2])
    if pt: 
        for x in Temp[1]: print '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(x[0][0],x[0][1],x[0][2],x[1][0],x[1][1],x[1][2])
        print
def Euc(a,b,s):
    #print a,b #Print Steps
    if b[2]==0: return [b[0],b[1],a[2]],s
    if b[2]==1: return b,s
    else:
        Q=a[2]/b[2]
        t=[a[n]-Q*b[n] for n in range(3)]
        a=b
        b=t
        return Euc(a,b,s+[[a,b]])
Euclid(7,5)
Euclid(26,3)
Euclid(1000,800,pt=1)
Euclid(5423,76357,pt=1)

# <codecell>


