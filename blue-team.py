#initializing the blue team and its interaction functions with the green team.

#description of the blue team:
    # 2. Blue Team: Similarly, blue team can push a counter-narrative and interact with green
#    team members. However, if they invest too much by interacting with a high certainty,
#    they lose their “energy level”. If they expend all their energy, the game will end. You
#    need to model this in way that the game keeps going on while the blue team is
#    changing the opinion of the green team members. Blue team also has an option to let
#    a grey agent in the green network. That agent can be thought of as a life line, where
#    blue team gets another chance of interaction without losing “energy”. However, the
#    grey agent can be a spy from the red team and in that case, there will be a round of
#    an inorganic misinformation campaign. In simple words, grey spy can push a potent
#    message, without making the red team lose followers.


class BlueTeam:
    def __init__(self, id, team, opinion, uncertainty, energy, potent):
        self.id = id
        self.team = team #
        self.opinion = opinion #opinion of the agent, 0 = undecided, 1 = pro, 2 = anti
        self.uncertainty = uncertainty # uncertainty is the amount of doubt the agent has about their opinion
        self.energy = energy #energy is the amount of energy the agent has to interact with the green team
        self.potent = potent #potent is the amount of potency the agent has to interact with the green team
        
    def green_interaction(green_team):
        for green_agent in green_team:
            if green_agent.uncertainty > 0:
                if self.potent > green_agent.uncertainty:
                    green_agent.uncertainty = 0
                else:
                    green_agent.uncertainty = green_agent.uncertainty - self.potent
                self.energy = self.energy - self.potent
            else:
                self.energy = self.energy - self.potent
        return green_team
    
    
