# #Game Scenario
# There are four teams involved: Red, Blue, Green and Grey.
# The scenario has been deliberately designed to represent the uneven playing field of the
# contested environment between the various teams. The scenario highlights the
# vulnerabilities of blue team in the contested information environment. The concept of blue
# and red teams is prevalent in cybersecurity related serious games or wargames. If you wish
# to get some background knowledge about the functioning of teams, you can read this article:
# https://csrc.nist.gov/glossary/term/red_team_blue_team_approach. However, this game is
# not related to cyber security, rather we are modelling the information environment in a
# country.
# Red and Blue teams are the major geopolitical players in this fictitious country.
# Red team is seeking geopolitical influence over Blue team. Of particular interest to Red team
# is influence over Green population and the Government. Blue is seeking to resist the Red
# teams growing influence in the country, and promote democratic government in the Green
# country.
# A key challenge faced by the Blue team, that will become apparent in the exercise, is that
# their democratic values are leveraged against them. They are vulnerable to some forms of
# manipulation, yet their rules-of-engagement do not allow them to respond in equal measure:
# there are key limitations in the ways in which they respond and engage in this unique
# battlespace. The Blue team is bound by legal and ethical restraints such as free media,
# freedom of expression, freedom of speech.
# The Green team lacks a diverse media sector, it is confused and there is a wide range of
# foreign news broadcasting agencies Green’s population has subscribed to. The Green
# population suffers from poor internet literacy, and the internet literacy can be modelled via
# pareto distribution. The government lacks resources to launch a decisive response to foreign
# influence operations and a lack of capability to discover, track and disrupt foreign influence
# activity.
# The Red team, an authoritarian state actor, has a range of instruments, tactics and
# techniques in its arsenal to run influence operations. The Green government can block
# websites and social media platforms and censor news coverage to its domestic population
# whilst maintaining the capability to run sophisticated foreign influence operations through
# social media.
# The Grey team constitutes foreign actors and their loyalties are not known.
# Election day is approaching and the Red team wants to keep people from voting.
# Population Model:
# An underlying network model that define the probability of nodes interacting with each other.
# Majority of the nodes, over 90%, will belong to green team and they depict the population of
# the country. A small percentage of nodes will be red, blue and grey. At the beginning grey
# nodes are not part of the network.
# Each green node/agent has an opinion and an uncertainty associated. In every simulation
# round nodes will interact with each other and affect each others’ opinions. The more
# uncertain an agent is, the more likely their opinion would change. The probability of
# interaction is not uniform across all nodes. Some nodes (for instance those in a household),
# may have a higher probability to interact.
# How teams are going to take turns:
# Teams are going to take turns one by one.

import csv

# 1. Red Team: You need to create function where red team (only 1 agent) is able to
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
import networkx as nx


def read_network():
    """
    This Function reads the node-attributes.csv file and creates a graph based on the attributes, assigning ID to each node and also the node's team.
    """
    G = nx.Graph()
    with open("node-attributes.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            G.add_node(row[0], team=row[1], opinion=row[2])
    return G


def main():
    print("Welcome to the game")
    print("Current Graph is: ")
    print(read_network())


# def game():
#     print("Game Started")
#     green_population = input("Enter the number of green agents: ")

#     #initialize the network with green population
#     green_team = initialize_network(green_population)

#     #choosing if it's AI vs AI or AI vs Human
#     print("Choose the mode of the game:")
#     print("1. AI vs AI")
#     print("2. AI vs Human")
#     mode = input("Enter your choice: ")
#     if mode == "1":
#         print("AI vs AI")
#         # start_game()
#     elif mode == "2":
#         human_team = input("Do you want to play as red team or blue team? (r/b): ")
#         if human_team == "r":
#             print("AI vs Human")
#             #initialize the red team
