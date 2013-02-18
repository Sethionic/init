# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #HowTo's
# 
# ##Graphs
# x = numpy.arange(0,2 * math.pi, 0.1)
# f1=map(lambda x: 5 * math.sin(x), x)
# f2=map(lambda x: 2 * math.sin(2*x), x)
# f3=map(lambda x: 1 * math.sin(3*x), x)
# pylab.plot(x,f1)
# pylab.plot(x,f2,'ro')
# pylab.plot(x,f3,'g--')
# pylab.show()
# 
# 
# LaTeX: $e^{i \omega t}$

# <codecell>

from IPython.core.display import *

global MathJax 
MathJax = True
def MDPL(string): display(Math(string)) if MathJax else display(Latex(string))

def add(x,y): return x+y

def comp_str(listofstrings): return reduce(add,listofstrings)

class math_expr(object):
   '''''Math Expression object'''''

   def __init__(self,arg1):
      '''''init takes arg: list of atoms, each atom being a compilable chunck of LaTeX expression'''''
      self.listofatoms = arg1

   def show(self):
      '''''Displays the content of the expression in mathmode'''''
      MDPL(comp_str(self.listofatoms))

   def replace(self,pos,newstr):
      '''''Replaces an atom with another atom'''''
      MDPL(comp_str(self.colouratoms([pos])))
      self.listofatoms[pos] = newstr
      MDPL(comp_str(self.colouratoms([pos],True)))

   def merge(self,positions):
      '''''Merges atoms: the input is a list of positions. The new atom is placed at the position of the foremost of the positions'''''
      MDPL(comp_str(self.colouratoms(positions)))
      temp = [ self.listofatoms[i] for i in positions ]
      positions.sort()
      positions.reverse()
      for i in positions: del self.listofatoms[i]
      self.listofatoms.insert(positions[-1],comp_str(temp))
      MDPL(comp_str(self.colouratoms([positions[-1]],True)))

   def split(self,pos,newatoms):
      '''''Splits atoms: replaces an atom in place with multiple sub atoms'''''
      MDPL(comp_str(self.colouratoms([pos])))
      del self.listofatoms[pos]
      templen = len(newatoms)
      while len(newatoms) > 0:
         self.listofatoms.insert(pos,newatoms.pop())
      MDPL(comp_str(self.colouratoms(range(pos, pos+templen),True)))

   def cancel(self,positions):
      '''''Cancels a bunch of terms: input a list of positions'''''
      MDPL(comp_str(self.colouratoms(positions)))
      positions.sort()
      positions.reverse()
      for i in positions: del self.listofatoms[i]
      self.fullshow()

   def move(self,posini,posfin):
      '''''Move atom at posini to posfin, pushing all others back'''''
      MDPL(comp_str(self.colouratoms([posini])))
      temp = self.listofatoms.pop(posini)
      self.listofatoms.insert(posfin if posfin < posini else posfin-1, temp)
      MDPL(comp_str(self.colouratoms([posfin if posfin < posini else posfin-1],True)))

   def colouratoms(self,positions,labelled=False):
      '''''Returns the list of atoms, but with selected terms coloured'''''
      temp = list(self.listofatoms)
      if labelled:
         self.labelatoms()
         temp = list(self.labeledatoms)
      for i in positions: temp[i] = "\color{red}{"+temp[i]+"}"
      return temp

   def labelatoms(self):
      '''''Label atoms by adding underbraces'''''
      self.labeledatoms = [ "\underbrace{" + self.listofatoms[i] + "}_{" + str(i) + "}" for i in range(len(self.listofatoms)) ]

   def fullshow(self):
      '''''Shows the content whilst labeling positions'''''
      self.labelatoms()
      MDPL(comp_str(self.labeledatoms))

# <codecell>

pprint=MDPL
#from IPython.core.display import display_latex as pprint

pprint("""\begin{tabular}{ l | c || r }
  1 & 2 & 3 \\
  4 & 5 & 6 \\
  7 & 8 & 9 \\
\end{tabular}""")

# <codecell>

#(Extended) Euclid Algorithm
#
def Euclid(a,b,ans=0,pt=0,retA=0):
    Temp=Euc([1,0,a],[0,1,b],[[['A1','A2','A3'],['B1','B2','B3']],[[1,0,a],[0,1,b]]])
    T=Temp[0]
    if ans:
        print '\n({0})({1})+({2})({3})={4}'.format(a,T[0],b,T[1],T[2])
    if pt: 
        for x in Temp[1]: print '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(x[0][0],x[0][1],x[0][2],x[1][0],x[1][1],x[1][2])
        print
    if retA:
        return [a,T[0],b,T[1],T[2]]
def Euc(a,b,s):
    #Main recursive loop
    if b[2]==0: return [b[0],b[1],a[2]],s
    if b[2]==1: return b,s
    else:
        Q=a[2]/b[2]
        t=[a[n]-Q*b[n] for n in range(3)]
        a=b
        b=t
        return Euc(a,b,s+[[a,b]])
#Example Runs
Euclid(3,59,ans=1,pt=1,retA=1)
#Euclid(4,9,pt=1)
#Euclid(26,3)
#Euclid(1000,800,pt=1)
#Euclid(5423,76357,pt=1)

# <codecell>

#Chinese Remainder Theorum
#Done, but only has LaTeX visual output so far
pprint=MDPL
def ChRem(A):
    M=reduce(lambda x,y:x*y,[i[1] for i in A])
    pprint( 'M={0}'.format(M))
    count=1;Ans=[];outS='';sumS=0
    for i in A:
        Ans=Ans+[[count,i[0],i[1],M/i[1],Euclid(M/i[1],i[1],retA=1)[1]%i[1]]]
        #print 'a({0})={1} m({0})={2} M/M({0})={3} c({0})={4}'.format(Ans[count-1][0],Ans[count-1][1],Ans[count-1][2],Ans[count-1][3],Ans[count-1][4])
        pprint('a_{{{0}}}={1},\ m_{{{0}}}={2},\ \\frac{{M}}{{M_{{{0}}}}}={3},\ c_{{{0}}}={4}'.format(Ans[count-1][0],Ans[count-1][1],Ans[count-1][2],Ans[count-1][3],Ans[count-1][4]))
        outS=outS+'({0}*{1}*{2})+'.format(Ans[count-1][3],Ans[count-1][4],Ans[count-1][1])
        sumS=sumS+(Ans[count-1][3]*Ans[count-1][4]*Ans[count-1][1])
        count=count+1
    pprint( outS[:-1] + ' = {0}'.format(sumS) )
    pprint( '= {0}\ mod\ {1}'.format(sumS%M,M) )
ChRem([[5,7],[7,11],[3,13]]);print
#ChRem([[2,4],[3,59]]);print
#ChRem([[2,7],[3,10]])

# <codecell>

#P1 Encryption/Decryption/Frequency Analysis
from binascii import *        #Hex conversion
from collections import deque #Queue
from collections import defaultdict as dd #Dynamic Dictionary
from string import Template   #Output formatting
import re

def type2(a):
    try:
        b=type(a)
    except:
        b='NULL'
    return b

def remDups(seq):
    seen = set()
    seen_add = seen.add
    return reduce(lambda x,y:x+y,[ x for x in seq if x not in seen and not seen_add(x)])

class Cipher:
    def __init__(self):
        pass
    def enc(self,s):
        print "No Encryption Algorithm Added"
    def dec(self,s):
        print "No Decryption Algorithm Added"

class MAS(Cipher):
    """Monoalphabetic Substitution Cipher"""
    def __init__(self,a,b):
        self.a=a
        self.b=b
        self.an=Euclid(a,26,retA=1)[1]
    def enc(self,s):
        return reduce(lambda x,y:x+y,[chr(((ord(p)-97)*self.a+self.b)%26+97) for p in s])
    def dec(self,s):
        return reduce(lambda x,y:x+y,[chr((((ord(p)-97)-self.b)*self.an)%26+97) for p in s])
    
class PF(Cipher):
    """Playfair Cipher"""
    def __init__(self,s):
        Temp=remDups(s.replace('q','')+'abcdefghijklmnoprstuvwxyz')
        Temp2=[]
        for i in range(5):
            Temp2=Temp2+[Temp[i*5:(i+1)*5]]
        self.Table=Temp2
    def printTable(self):
        for i in self.Table:
            print '{0}'.format(str(i))

#English frequency data:
#http://jnicholl.org/Cryptanalysis/Data/EnglishData.php

class Cgram:
    def __init__(self):
        Monograms=self.loadgram('monogram.dat')
        Digram=self.loadgram('digram.dat')
        Trigram=self.loadgram('trigram.dat')
        Polygram={}#Not implemented yet
        self.grams=[Monograms,Digram,Trigram,Polygram]
    def loadgram(self,path):
        temp=dd(int)
        with open(path) as f:
            for i in f:
                res=i.split()
                temp[res[0]]=res[1]
        return temp
    def search(self,s):
        self.rep=dd(int)
        for i in range(3):
            self.subsearch(s,i+1)
        print self.rep
    def mapper(self):
        #Throw the found grams into a maxheap and pair them with their correponding highest
        #freq contender for each size. for each char in each gram, raise the confidence of
        #a mapping by one
        #e.g. 'ABC' matches 'CRE' and 'AB' matches 'TE': {'A':[['C',1]['T',1]],'B':[[R,1],[E,1]],etc...}
        #When mapping is complete, look for highest confidences and create a decoder dict to run the
        #ciphertext through
        decodex=dd(dd) #Dictionary of dictionaries of char:confidence parings
        #Use later for adding to decodex: """try: decodex[A][B]+=1 ; except decodex[A][B]=1"""
        heap
        ##### denotes something missing
        #####NEED to sort everything largest to smallest frequency
        for i in range(3): #i is the generated {mono,di,tri}graph set
            for j in self.rep[i+1].keys(): #j is each entry in a given graph set
                ####pop the next highest as j2
                for k in range(len(j)):
                    try:
                        self.decodex[j[k]][j2[k]]+=1
                    except:
                        self.decodex[j[k]][j2[k]]=1
        #By the end of this function, there should be character mappings based on frequency comparisons
        #Still need to translate the confidence values to most likely characters [self.makeMap]
    def makeMap(self):
        pass
    def subsearch(self,s,n):
        #self.rep=dd(int)
        t1=s.lower().split(' ')
        for s in t1:
            for iter in range(n):
                for i in [(s[iter+i:iter+i+n]) for i in xrange(0, len(s), n) ]:
                    if len(i)==n: self.rep[i]+=1


    

# <codecell>

#print "Testing MAS"
TEST = MAS(9,17)
#print TEST.dec("crwwz")
#print TEST.enc("happy")
#Blah=unhexlify(hexlify("Test"))
#print "\nTesting PF"
#TEST = PF('testerstesting')
#TEST.printTable()
#print TEST.dec("blahblahtesttest")
#print TEST.enc("happy")
print "\nTesting Freq:\n"
pt='Episode IV, A NEW HOPE It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire. During the battle, Rebel spies managed to steal secret plans to the Empire’s ultimate weapon, the DEATH STAR, an armored space station with enough power to destroy an entire planet. Pursued by the Empire’s sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy….'
pt=re.sub('[^a-z]','',pt.lower())
ct=TEST.enc(pt)
tt=TEST.dec(ct)
print 'Plaintext:',pt
print 'Ciphertext:',ct
print 'UnCiphered:',tt
Anyl=Cgram()
Anyl.search(ct)

#testdict=calcf(temp,3)
#temp=[]
#for i in testdict.keys():
#    temp+=[[testdict[i],i]]
#temp.sort()
#print temp

# <codecell>

print Anyl.grams
#import scipy
#Euclid(5,7,retA=1)

# <codecell>


