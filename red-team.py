#this is used to create initializations for the red team, and its interaction functions:

import random
import numpy as np
import matplotlib.pyplot as plt


class RedTeam:
    
#     1. Red Team: You need to create function where red team (only 1 agent) is able to
#    interact with all members of the green team. The agent affects the opinions and
#    uncertainty of the green team during the interaction. The catch is that you need to
#    select from 5 levels of potent messaging. If the red team decides to disseminate a
#    potent message, during the interaction round, the uncertainty variable of the red team
#    will assume a high value. A highly potent message may result in losing followers i.e.,
#    as compared to the last round fewer green team members will be able to interact with
#    the red team agent. However, a potent message may decrease the uncertainity of
#    opinion among people who are already under the influence of the red team (meaning
#    they are skeptical about casting a vote). You need to come up with intelligent
#    equations so that red team improves the certainity of opinion in green agents, but at
#    the same time does not lose too many green agents. Think of it as a media channel
#    trying to sell their narrative to people. However, if they may big, claim, lie too much,
#    they might lose some neutral followers which they could indoctrinate with time.

    def __init__(self, id, team, opinion, uncertainty, energy, potent):
        self.id = id
        self.team = team
        self.opinion = opinion
        self.uncertainty = uncertainty
        self.energy = energy
        self.potent = potent
        
        
        
    def initialize_red_team(self):
        # initialize red team agent
        self.id = 0
        self.team = 1
        self.opinion = 0
        self.uncertainty = 0
        self.energy = 100
        self.potent = 0
        
        # assign potent messaging levels
        # assign a random potent messaging level to the red team agent
        self.potent = random.randint(1,5)
        
        return self.id, self.team, self.opinion, self.uncertainty, self.energy, self.potent
    
    def red_team_interaction(self, green_team):
        # red team agent interacts with all members of the green team
        # the agent affects the opinions and uncertainty of the green team during the interaction
        # the catch is that you need to select from 5 levels of potent messaging
        # if the red team decides to disseminate a potent message, during the interaction round, the uncertainty variable of the red team will assume a high value
        # a highly potent message may result in losing followers i.e., as compared to the last round fewer green team members will be able to interact with the red team agent
        # however, a potent message may decrease the uncertainity of opinion among people who are already under the influence of the red team (meaning they are skeptical about casting a vote)
        # you need to come up with intelligent equations so that red team improves the certainity of opinion in green agents, but at the same time does not lose too many green agents
        # think of it as a media channel trying to sell their narrative to people
        # however, if they may big, claim, lie too much, they might lose some neutral followers which they could indoctrinate with time
        
        # red team agent interacts with all members of the green team
        for green_agent in green_team:
            # the agent affects the opinions and uncertainty of the green team during the interaction
            # the catch is that you need to select from 5 levels of potent messaging
            # if the red team decides to disseminate a potent message, during the interaction round, the uncertainty variable of the red team will assume a high value
            # a highly potent message may result in losing followers i.e., as compared to the last round fewer green team members will be able to interact with the red team agent
            # however, a potent message may decrease the uncertainity of opinion among people who are already under the influence of the red team (meaning they are skeptical about casting a vote)
            # you need to come up with intelligent equations so that red team improves the certainity of opinion in green agents, but at the same time does not lose too many green agents
            # think of it as a media channel trying to sell their narrative to people
            # however, if they may big, claim, lie too much, they might lose some neutral followers which they could indoctrinate with time
            
            # if the red team decides to disseminate a potent message, during the interaction round,
            
            # the uncertainty variable of the red team will assume a high value
            # a highly potent message may result in losing followers i.e., as compared to the last round fewer green team members will be able to interact with the red team agent
            
            #check if the red team agent is potent
            if self.potent > 0:

                # if the red team agent is potent, then the uncertainty variable of the red team will assume a high value
                self.uncertainty = 1
                
                # a highly potent message may result in losing followers i.e., as compared to the last round fewer green team members will be able to interact with the red team agent
                # if the red team agent is potent, then the number of green team members that can interact with the red team agent will be reduced
                # the number of green team members that can interact with the red team agent will be reduced by the potent messaging level of the red team agent
                green_team = green_team[:-self.potent]
                
                    