
import math
import time
import random
import collections
from collections import Counter
from Utility import *

#add noise
noise = .02
memory = 6
growth_constant = .02

# Define some colors
black    = (   0,   0,   0)
grey     = (   128,   128,   128)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
 
#likelyhood of playing rabbit on random choice
playRabbit = .5
 
#make a key
def makeKey(loc):
    return loc[0]*100 + loc[1]
 
def most_common(lst):
    return max(set(lst), key=lst.count)


#enumerations
what_I_produce = 0
what_I_consume = 1
what_I_carry = 2
 
#good i produce, good i consume, good I carry
trade_interests = [("A","B","A"),("B","A", "B"),("C","A", "C"),("A","C", "A"),("B","C", "B"),("C","B", "C") ]

class TradeHistory(object):
     def __init__(self):
         self.giver = None
         self.receiver = None
         self.what_was_given = "A"
         self.what_was_received = "A"
         
         
# base agent class
class AgentBase(object):
    def __init__(self): 
        
        #goods
        self.m1 = growth_constant
        self.m2 = growth_constant
        self.m3 = growth_constant
          
        #total  
        self.History = [] 
        self.Location = [0,0]
        self.Color = grey 
        self.Moves = [] #store payoff per play of   
        self.Neighbors = [] #store agent by id
               
        #choose random trade interests
        val = random.randint(0,len(trade_interests)-1)
        self.TradeInterests = trade_interests[val]
        self.AgentTrades = 0 
        self.Utility = 0
        
        self.Cost = {}
        self.update_cost()
        
 
    #update costs based on new m values
    def update_cost(self):
        self.Cost["A"]= 0 + (0/(2+self.m1)) 
        self.Cost["B"]=.5 + (1/(2+self.m2)) 
        self.Cost["C"]=.25+ (1/(2+self.m3)) 
        return
        
    
    #get m value
    def GetM(self, value):
        if value == 'A':
            return self.m1
        if value == 'B':
            return self.m2
        if value == 'C':
            return self.m3
        
        
    #generate a utility value
    def SetUtility(self, utility):
        
        self.Utility += utility
        #get what you consume
        if self.TradeInterests[what_I_produce]=='A':
            self.m1 += 1
        if self.TradeInterests[what_I_produce]=='B':
            self.m2 += 1
        if self.TradeInterests[what_I_produce]=='C':
            self.m3 += 1
            
        self.update_cost()
      
    
    #generate a color for the display.
    def Update(self):  
        
        #utility is 1-cost, use this to set a color spectrum if it is decided to use a matrix
        util = 1-self.Cost[self.TradeInterests[what_I_produce]]
        
        if self.TradeInterests[what_I_produce]=='A':
            self.Color = (0, util*255, 0)
        if self.TradeInterests[what_I_produce]=='B':
            self.Color = (util*255, 0,  0)
        if self.TradeInterests[what_I_produce]=='C':
            self.Color = (0,  0, util*255)      

        
    
    
#create local agent class
class AgentWithLocalNeighbors(AgentBase):
    def __init__(self, numAgents):
        AgentBase.__init__(self)

#create random agent neighbor class
class AgentWithRandomNeighbors(AgentBase):
    def __init__(self, numAgents):
        AgentBase.__init__(self)
    
 