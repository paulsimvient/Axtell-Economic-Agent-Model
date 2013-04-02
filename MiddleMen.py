 

'''
Paul Cummings
CS 605
Dr. Robert Axtell
'''
import math
import time
import random
import collections
import csv
from operator import itemgetter
from Agents import * 
import matplotlib.pyplot as plt	# to enable plot of histogram
import numpy as np
 
 

#all agents
Agents = []
numAgents = 500
  
#trials
trials = 0
#will be the agents that participated in trades
trade_history = [ ]

#statistics 
statistics = []

#threshold for trading
some_threshold_for_trading = .55
 
 
def ChooseAnAgent():
    #get agent
    val = random.randint(0,len(Agents)-1)
    return Agents[val]


#choose an alternate to trade with
def ChooseAlt(other_player):
    
    #get all trades
    numTrades = len(Trades)
    if numTrades == 0:
        return ChooseAnAgent()
        
    it_dictionary = Counter(Trades)
 
    #if their are fewer than 10% of agents traded move on 
    length_array = len(Trades)
    num_to_compare = (numAgents*.80)
    if  length_array < num_to_compare:
        return ChooseAnAgent()
         
    #NOTE: This is not complete
    items = [(v, k) for k, v in it_dictionary.items()]
    items.sort()
    items.reverse()             # so largest is first
    items = [(k, v) for v, k in items]  
    

    #do probability
    #[2,3,4,5]
    #[2/14,3/14,4/14,5/14]
    #cumulatative
    
    return items[0][0]


#essentially is what the player wants to consume the same as what other wants to produce?
def potentialTrade(player1, player2):
    return player1.TradeInterests[what_I_consume] == player2.TradeInterests[what_I_produce] or player2.TradeInterests[what_I_consume] == player1.TradeInterests[what_I_produce]
    
def doWantToEat(player1, player2):
    if player2.TradeInterests[what_I_carry] == player1.TradeInterests[what_I_consume]:
        return True
    return False
    
    
#determine how many trade neighbors I have
def numOpposite(player):
    
    num_opposite = 0
    #sample 3
    for i in player.Neighbors: 
        # find number of potential trades with neighbors
        if potentialTrade(i,player):
            num_opposite += 1
                
    return num_opposite
    
 
trades = [("A","B"), ("B","A"), ("B","A"), ("B","A"), ("B","A"), ("C","A"), ("B","A"), ("B","A"), ("B","A")]
   
#sample population and get 
def SamplePopulation(player1):
    
   
    rSampleNum = 25
    sampled_trades = []
    
    #sampled data
    for i in range(0,rSampleNum):
        if i < len(trade_history):
            sampled_trades.append(trade_history[i])
        
    if len(sampled_trades) == 0:
        return None
    
    
    list_trades = [] 
    #iterate through sampled traded
    for i in sampled_trades:
         giver = i.giver #agent
         receiver = i.receiver #agent
    
         was_given = i.what_was_given #value "A,B,C"
         was_received =  i.what_was_received #value "A,B,C"

         list_trades.append((was_given, was_received))
    
    
    it_dictionary = Counter(trades)  
   
    dict_probabilities = {}
    #generate a list of probabilities
    for k1, v1 in it_dictionary.iteritems() : 
       dict_probabilities[k1] = v1/len(sampled_trades)*1.0
       
  
    return dict_probabilities
 
 
#sample costs
def Sample_Cost(tuple_give_receive):
    
    rSampleNum = 25
    sampled_trades = []
    
    #sampled data
    for i in range(0,rSampleNum):
        if i < len(trade_history):
            sampled_trades.append(trade_history[i])
        
    
    list_ms = [] 
    #iterate through sampled traded
    for i in sampled_trades:
        
        giver = i.giver #agent
        receiver = i.receiver #agent
         
        tple = (was_given, was_received)
        if tple == tuple_give_receive:
            carry = receiver.TradeInterests[what_I_carry]
            list_ms.append(receiver.GetM(carry))
            mean = np.mean(list_ms)
    
    return mean
  
#determine if agent wants to trade
def AgentsWantToTrade(player1, player2):
  
    ET_Eat = 0
     
    if doWantToEat(player1, player2):
 
    #what is his cost for him to consume
        value = player2.TradeInterests[what_I_carry] #(carry)
        my_cost = player1.Cost[value]    
    
        value = player1.TradeInterests[what_I_carry] #(carry)
        his_cost = player2.Cost[value] 
    
        ET_Eat = 1-(my_cost + his_cost)/2.0
        ET =  ET_Eat  
         
    else: 
        
        prob_dictionary = SamplePopulation(player1)
        if prob_dictionary != None:
            
            receive = player2.TradeInterests[what_I_carry]
            give = player1.TradeInterests[what_I_consume]
            
            probability = prob_dictionary[(give,receive)]
            
            #formula = p[1-(good_Im_eating + (expected_cost)/2)]
            good_Im_eating = player1.TradeInterests[what_I_consume]
            expected_cost = Sample_Cost((give,receive))
            
            ET_No_Eat = probability[1-(good_Im_eating + (expected_cost)/2.0)]
            ET = ET_No_Eat
      
      
            #separate calculation for value of not trading
            prob_dictionary = SamplePopulation(player1)
              
            receive = player1.TradeInterests[what_I_carry]
            give = player1.TradeInterests[what_I_consume]
            
            probability = prob_dictionary[(give,receive)]
            
            #formula = p[1-(good_Im_eating + (expected_cost)/2)]
            good_Im_eating = player1.TradeInterests[what_I_consume]
            expected_cost = Sample_Cost((give,receive))
            
            EN = probability[1-(good_Im_eating + (expected_cost)/2.0)]
           
            if ET > EN:
                return True
            
        return False
    

def DoTrade(player1, player2):
    #now benefit of trading
        #he wants to barter with me 
   
    #how do we know consumption good or carry
    if player2.TradeInterests[what_I_carry] == player1.TradeInterests[what_I_consume]:
        # What does it cost for him to trade
        value = player2.TradeInterests[what_I_carry] 
        my_cost = player1.Cost[value]        
    
        #now for me
        value = player1.TradeInterests[what_I_carry]
        his_cost = player2.Cost[value]   
        
        #get shared costs
        #NOTE: Won't work if mycost + his > 1
        my_utility = 1 - (my_cost +  his_cost)/(2*1.0)
        
        #update inventory item
        player1.TradeInterests[what_I_carry] = player1.TradeInterests[what_I_produce] 
  
        player1.SetUtility(my_utility) 
     
     #NOTE: THis needs updating 
     
    #instance of trade history
    trade_history = TradeHistory() 
    trade_history.giver = player1
    trade_history.receiver = player2
    
    total_trades.append(trade_history)
     

    #store this for data reference
    statistics.append((player1.TradeInterests[what_I_produce], player2.TradeInterests[what_I_consume])) 
    
    
    it_dictionary = Counter(statistics)
    sorted(it_dictionary, key=lambda key: it_dictionary[key])
   
    #print this
    print it_dictionary.most_common(4)   
 
    
class playGame(object):
    
    def __init__(self):
        self.trials = 0 
       
    def BuildAgents(self, row, height, sim_type_neighbor):       
        #build the agents
          
        agent = None
        
        while True: 
            
            #get location
            location = [int(random.uniform(0,row)), int(random.uniform(0,height))]
            
            #check to see if it's taken
            for i in Agents:
                if i.Location == location:
                    continue
 
            #this is basically to look at either random neighbor locations on a lattice or local neighbors on a grid
            if sim_type_neighbor == True:
                agent = AgentWithLocalNeighbors(numAgents) 
            else:
                agent = AgentWithRandomNeighbors(numAgents) 

            #set location
            agent.Location = location    
            
            #add new agent           
            Agents.append(agent)
            
            #done adding new agents
            if len(Agents) == numAgents:
                break
         
        #set neighbors   
        self.getNeighbors(sim_type_neighbor)
        
 
    #get agent neighbors
    def getNeighbors(self, sim_type_neighbor):
        
        arrayOffsets = [(-1,1),  (0,1),  (1,1),
                        (-1,0),          (1,0),
                         (-1,-1),(0,-1), (1,-1)]  
       
           
        for i in Agents:
            #get a set of neighbors close by you
            arrayWidth = i.Location[0]
            arrayHeight = i.Location[1]
             
             #nearest neighbor
            if sim_type_neighbor: 
                for r in arrayOffsets:
                    #get location in array
                    loc = [arrayWidth + r[0],
                           arrayHeight+ r[1]]
                    
                    agent_at_location = self.agentLoc(loc)
                    if agent_at_location != None:
                        i.Neighbors.append(agent_at_location)
            else:
                for r in range(0,8):
                    myAgent =  Agents[int(random.uniform(0,1)*numAgents)-1]               
                    i.Neighbors.append(myAgent)
                

    def agentLoc(self, location):
        #add a neighbor
        for j in Agents:
            if j.Location == location:
                return j
           
        return None

    
    #agent tick function
    def AgentNext(self):
         
        #get a random agent
        player1 = ChooseAnAgent()
        player2 = ChooseAnAgent()
        if player1 == player2:
            return
        
        #see if agent wants to trade
        if AgentsWantToTrade(player1, player2):
            DoTrade(player1, player2)
         
        #update internal states
        player1.Update()
        player2.Update()

   
   
 
def Play():       
    #play the middle men game
    middleMen = playGame()
    
    #build agent by type 
    middleMen.BuildAgents(40, 40, False)
    
    
    done = False
    while done==False:
        #do next agent move   
          middleMen.AgentNext()        
          
          
Play()