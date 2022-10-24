import csv
import math
import os
import random
import sys

print(sys.setrecursionlimit(2000))
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Potency of messaging levels for red team agent (1-5)
# 1 = low potency
# 5 = high potency
last_choice = 0
blue_energy = 100
grey_used = 0
red_followers = 0
MINIMUM_UNCERTAINTY = -1
MAXIMUM_UNCERTAINTY = 1
turns = 10
last_r_potency = 0
last_b_potency = 0


def networkanalysis():
    """
    This function reads the network-2.csv  and creates a dictionary.
    In each line, if it's 1,2 add 2 to 1's neighbors and 1 to 2's neighbors
    """
    list_edges = []
    with open("network-2.csv") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for row in lines[1:]:
            row = row.split(",")
            list_edges.append((int(row[0]), int(row[1])))

    return list_edges
    # create a copy of graph and add edges from list_edges
    # print(list_edges)
    # G = nx.DiGraph()
    # G.add_edges_from(list_edges)
    # nx.draw(G)
    # plt.show()


def read_network():
    """
    This Function reads the node-attributes.txt file and creates a graph based on the attributes, assigning ID to each node and also the node's team.
    """
    G = nx.Graph()
    with open("node-attributes.txt") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for row in lines[1:]:
            row = row.split(",")
            G.add_node(int(row[0]), team=row[1])
    # print(G.nodes(data=True))
    return seperate_teams(G)


def seperate_teams(graph):
    """
    This function takes the initial graph and return three separate graphs for each team
    i.e. Green, Blue, Red and Grey (if grey it also includes if they are good or bad)
    """
    green_team = nx.Graph()
    red_team = nx.Graph()
    blue_team = nx.Graph()
    grey_team = nx.Graph()
    for node in graph.nodes(data=True):
        if node[1]["team"] == "green":
            green_team.add_node(node[0], team=node[1]["team"])
        elif node[1]["team"] == "red":
            red_team.add_node(node[0], team=node[1]["team"])
        elif node[1]["team"] == "blue":
            blue_team.add_node(node[0], team=node[1]["team"])
        elif node[1]["team"].split("-")[0] == "grey":
            grey_team.add_node(node[0], team=node[1]["team"])

    return green_team, red_team, blue_team, grey_team


def initialize_green_team(green_team):
    """
    This function takes the green team, creates a new graph with the same nodes and assigns a random opinion(X) to each node and random uncertainty(U) to each node
    in the range [-1,1]
    x : 1 or 0, 1 = pro-voting, 0 = anti-voting
    """
    new_green_team = nx.Graph()
    for node in green_team.nodes(data=True):
        new_green_team.add_node(
            node[0], X=random.randint(0, 1), U=round(random.uniform(-1, 1), 1), F=1
        )

    return new_green_team


def visualize_graph(graph):
    """
    This function takes a graph and visualizes it
    """
    new_graph = nx.Graph()
    blue_count = 0
    red_count = 0
    for node in graph.nodes(data=True):
        color = ""
        if node[1]["X"] == 1:
            color = "blue"
            blue_count += 1
        else:
            color = "red"
            red_count += 1
        new_graph.add_node(node[0], color=color)

    # Visualize the graph with the X values as the node color, show the edges and the node labels
    nx.draw(
        new_graph,
        node_color=[node[1]["color"] for node in new_graph.nodes(data=True)],
        with_labels=True,
    )
    # label the graph with the number of blue and red nodes
    plt.title("Blue: " + str(blue_count) + " Red: " + str(red_count))

    plt.show()


def set_red_followers(green_team):
    """_summary_: This function takes the green team and assigns the number of followers from the green team"""
    global red_followers
    # Calculate the number of followers for the red agent
    for node in green_team.nodes(data=True):
        if node[1]["F"] == 1:
            red_followers += 1


def check_game_status():
    """
    This function checks the status of the game and returns the status of the game
    """
    if red_followers <= 0:
        print("Red agent has lost all their followers")
        return True
    if blue_energy <= 0:
        print("Blue agent has no more energy")
        return True
    else:
        return False


def end_game(green_team):
    """
    This function takes the status of the game and prints the winner
    """

    blue_count, red_count = count_nodes(green_team)
    if blue_count > red_count:
        print("Blue agent has won")
    elif red_count > blue_count:
        print("Red agent has won")
    else:
        print("It's a tie")


def count_nodes(green_team):
    """
    This function takes the green team and counts the number of green nodes with either X = 1 or X = 0
    """
    blue_count = 0
    red_count = 0
    for node in green_team.nodes(data=True):
        if node[1]["X"] == 1:
            blue_count += 1
        else:
            red_count += 1
    return blue_count, red_count


def green_interaction(green_graph):
    """
    A node's intent to vote can be determined by the X value, if X = 1, then the node is pro-voting, if X = 0, then the node is anti-voting.
    This function simulates the green-to-green interaction, where each node interacts with its neighbours and updates its opinion and uncertainty.
    For e.g. for two nodes A and B, if U(A) > U(B), it changes its opinion to that of A and uncertainity is calculated using the function.

    Important:
    Rules:
        1. If both the nodes have same opinion, the X remains same but the U changes, U = U1 + U2/2.
        2. If both the nodes dont have the same opinion, the X changes to the opinion of the node with higher U and the U is calculated using the function.
    """

    networkability = networkanalysis()

    for edge in networkability:
        first_node = edge[0]
        second_node = edge[1]

        # First Case : Compare their Opinion.
        if green_graph.nodes[first_node]["X"] == green_graph.nodes[second_node]["X"]:
            # In this case, the opinion remains the same but the uncertainty changes and
            # they become more certain about their opinion
            green_graph.nodes[first_node]["U"] = (
                green_graph.nodes[first_node]["U"] - green_graph.nodes[second_node]["U"]
            ) / 2
            green_graph.nodes[second_node]["U"] = (
                green_graph.nodes[first_node]["U"] - green_graph.nodes[second_node]["U"]
            ) / 2

        # Second Case : Compare their Uncertainty
        elif green_graph.nodes[first_node]["U"] < green_graph.nodes[second_node]["U"]:
            # In this case, the opinion of the first node is taken and the uncertainty is calculated using the function
            green_graph.nodes[second_node]["X"] = green_graph.nodes[first_node]["X"]
            green_graph.nodes[second_node]["U"] = calculate_uncertainty(
                green_graph.nodes[first_node]["U"], green_graph.nodes[second_node]["U"]
            )

        elif green_graph.nodes[first_node]["U"] > green_graph.nodes[second_node]["U"]:
            # In this case, the opinion of the second node is taken and the uncertainty is calculated using the function
            green_graph.nodes[first_node]["X"] = green_graph.nodes[second_node]["X"]
            green_graph.nodes[first_node]["U"] = calculate_uncertainty(
                green_graph.nodes[second_node]["U"], green_graph.nodes[first_node]["U"]
            )

    return green_graph


def calculate_uncertainty(U1, U2):
    """
    This function calculates the uncertainty of a node based on the uncertainty of the other node.
    """
    return (U1 - U2) / 2


def assigning_agents(r_agent, b_agent):
    """
    This function initializes the red and blue agents with their respective opinions and uncertainty.

    U(R) = -1 and U(B) = -1
    X(R) = 0 and X(B) = 1
    """
    for node in r_agent.nodes(data=True):
        r_agent.nodes[node[0]]["X"] = 0
        r_agent.nodes[node[0]]["U"] = -1

    for node in b_agent.nodes(data=True):
        b_agent.nodes[node[0]]["X"] = 1
        b_agent.nodes[node[0]]["U"] = -1

    return r_agent, b_agent


def main():
    """
    Main function that runs the simulation
    """

    # print("Welcome to the game")

    # print("Current Graph is: ")

    green_team, red_agent, blue_agent, grey_team = read_network()

    # print("Initialising the green team assigning random opinions and uncertainty")

    # print("Beep Boop")

    # print("Green Team is: ")

    green_team = initialize_green_team(green_team)

    set_red_followers(green_team)
    print("Total Green Nodes: ", green_team.number_of_nodes())
    print("Red Followers are: ")
    print(red_followers)
    run_sim(green_team)


def count_followers(green_team):
    fws = 0
    for nodes in green_team.nodes(data=True):
        if nodes[1]["F"] == 1:
            fws += 1
    return fws


def red_sim(g_team, potency):
    # potency_dire = {1: -0.2, 2: -0.4, 3: -0.6, 4: -0.8, 5: -1}
    # uncertainty = potency_dire[potency]
    for node in g_team.nodes(data=True):
        x, u, f = (
            g_team.nodes[node[0]]["X"],
            g_team.nodes[node[0]]["U"],
            g_team.nodes[node[0]]["F"],
        )
        x, u, f = red_interaction(x, u, potency, f)
        g_team.nodes[node[0]]["X"] = x
        g_team.nodes[node[0]]["U"] = u
        g_team.nodes[node[0]]["F"] = f
    return g_team


def red_interaction(opinion, uncertainty, potency, follower):
    if follower == 1:
        if opinion == 1:
            if uncertainty >= -1.0 or uncertainty <= -0.5:
                if potency > 2:
                    uncertainty = -1
                    follower = 0
                if potency in range(1, 2):
                    uncertainty = min(uncertainty - 0.2, -0.8)
                    dict_un = {1: 0.55, 2: 0.65, 3: 0.75}
                    follower = random.choices(
                        [0, 1], weights=[dict_un[potency], 1 - dict_un[potency]], k=1
                    )[0]

            if uncertainty > -0.5 or uncertainty <= 0:
                if potency > 3:
                    uncertainty = uncertainty + 0.2
                    dict_un = {4: 0.35, 5: 0.45}
                    follower = random.choices(
                        [0, 1], weights=[dict_un[potency], 1 - dict_un[potency]], k=1
                    )[0]
                elif potency in range(1, 3):
                    uncertainty = uncertainty + 0.1
                    dict_un = {1: 0.05, 2: 0.1, 3: 0.15}
                    follower = random.choices(
                        [0, 1], weights=[dict_un[potency], 1 - dict_un[potency]], k=1
                    )[0]
            if uncertainty > 0 and uncertainty <= 0.5:
                if potency > 3:
                    dict_un = {4: 0.4, 5: 0.5}
                    uncertainty = uncertainty + dict_un[potency]
                elif potency in range(1, 3):
                    dict_un = {1: 0.15, 2: 0.25, 3: 0.35}
                    uncertainty = uncertainty + dict_un[potency]
            if uncertainty > 0.5 and uncertainty <= 1:

                if potency > 2:
                    opinion = 0
                if potency == 1:
                    opinion = random.choices([0, 1], weights=[0.8, 0.2], k=1)[0]

        if opinion == 0:
            if uncertainty >= -1.0 or uncertainty <= 0:
                un_dict = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5}
                uncertainty = min(uncertainty - un_dict[potency], -1)
            if uncertainty > 0 and uncertainty <= 1:
                un_dict = {1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
                uncertainty = uncertainty - un_dict[potency]

    return opinion, uncertainty, follower


def blue_sim(g_team, potency, agent_used=False):
    # potency_dire = {1: -0.2, 2: -0.4, 3: -0.6, 4: -0.8, 5: -1}
    turn = 10
    energy_dir = {
        1: 100 / turn - 1.5,
        2: 100 / turn - 0.5,
        3: 100 / turn + 1.5,
        4: 100 / turn + 2.5,
        5: 100 / turn + 3.5,
    }
    a, b = count_nodes(g_team)
    tot_pop = a + b
    # uncertainty = potency_dire[potency]
    Energy_Used = 0
    for node in g_team.nodes(data=True):
        x, u = g_team.nodes[node[0]]["X"], g_team.nodes[node[0]]["U"]
        x, u = blue_interaction(x, u, potency)
        g_team.nodes[node[0]]["X"], g_team.nodes[node[0]]["U"] = x, u
    if not agent_used:
        Energy_Used = energy_dir[potency]

    return g_team, Energy_Used


def blue_interaction(opinion, uncertainty, potency):

    if opinion == 0:
        if uncertainty >= -1 or uncertainty <= -0.5:
            if potency > 3:
                uncertainty += 0.5

            if potency in range(1, 3):
                uncertainty = uncertainty + 0.2
                # dict_un = {1: 0.55, 2: 0.65, 3:0.75}

        if uncertainty > -0.5 or uncertainty <= 0:
            if potency > 3:
                uncertainty = uncertainty + 0.2
                # dict_un = {4: 0.35, 5:0.45}
                # follower = random.choices([0, 1], weights=[dict_un[potency], 1-dict_un[potency]], k=1)[0]
            elif potency in range(1, 3):
                uncertainty = uncertainty + 0.1
                # dict_un = {1: 0.05, 2: 0.1, 3: 0.15}
                # follower = random.choices([0, 1], weights=[dict_un[potency], 1-dict_un[potency]], k=1)[0]
        if uncertainty > 0 and uncertainty <= 0.5:
            if potency > 3:
                dict_un = {4: 0.4, 5: 0.5}
                uncertainty = uncertainty + dict_un[potency]
            elif potency in range(1, 3):
                dict_un = {1: 0.15, 2: 0.25, 3: 0.35}
                uncertainty = uncertainty + dict_un[potency]
        if uncertainty > 0.5 and uncertainty <= 1:
            un_dict = {
                1: 0.05,
                2: 0.07,
                3: 0.1,
                4: 0.2,
                5: 0.3,
            }
            uncertainty = uncertainty + un_dict[potency]
            opinion = 1

    if opinion == 1:
        if uncertainty >= -1.0 or uncertainty <= 0:
            un_dict = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4, 5: 0.5}
            uncertainty = min(uncertainty - un_dict[potency], -1)
        if uncertainty > 0 and uncertainty <= 1:
            un_dict = {1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
            uncertainty = uncertainty - un_dict[potency]

    return opinion, uncertainty


def count_sim_score(green_team, agent, potency, grey_used=False):
    global turns
    global blue_energy
    Green_Copy = green_team.copy()
    followers = red_followers
    bb_energy = blue_energy
    voters_early, anti_voters_early = count_nodes(green_team)
    score = 0
    if agent == "red":
        Green_Copy = red_sim(Green_Copy, potency)
        follower_count = count_followers(Green_Copy)
        voters_count, anti_voters_count = count_nodes(Green_Copy)
        follower_diff = followers - follower_count
        anti_voter_diff = anti_voters_count - anti_voters_early
        # formula to count the score based on the difference in followers and anti-voters
        score = anti_voter_diff - ((follower_diff / followers) * 0.25)

    if agent == "blue":
        Green_Copy, energy_count = blue_sim(Green_Copy, potency, grey_used)
        voter_count, anti_voter_count = count_nodes(Green_Copy)
        energy_diff = bb_energy - energy_count
        voter_diff = voter_count - voters_early
        # score based on current_blue energy, energy_diff and voter_diff and how many turns are left
        score = voter_diff - ((energy_diff / bb_energy) * 0.25) - ((turns / 100) * 0.25)

    return score


def set_red(green_team):
    r_f = 0
    for nodes in green_team.nodes(data=True):
        if green_team.nodes[nodes[0]]["F"] == 1:
            r_f += 1
    return r_f


def run_sim(green_team):
    global turns
    global blue_energy
    global last_b_potency
    global last_r_potency
    while turns > 0:
        if not check_game_status():
            turns -= 1
            r_potency = minimax(green_team, "red", 0, 5, True)
            last_r_potency = r_potency
            b_potency, grey_used = minimax(green_team, "blue", 0, 5, True)
            last_b_potency = b_potency
            green_team = red_sim(green_team, r_potency)

            green_team, energy_used = blue_sim(green_team, b_potency, grey_used)
            blue_energy -= energy_used

            green_team = green_interaction(green_team)
            rf = set_red(green_team)

            print(
                "Turns left: ",
                turns,
                "Blue Energy left: ",
                blue_energy,
                "Red Followers: ",
                rf,
                "Voters: ",
                count_nodes(green_team)[0],
                "Anti-Voters: ",
                count_nodes(green_team)[1],
                "blue potency: ",
                b_potency,
                "red potency: ",
                r_potency,
                "grey used: ",
                grey_used,
            )
        else:
            end_game(green_team)
            break
    end_game(green_team)


def minimax(g_team, agent, depth, max_depth, maximizingPlayer):
    if agent == "red":
        best_score = -math.inf
        best_potency = 0
        for i in range(1, 6):
            if i == last_r_potency:
                continue
            score = count_sim_score(g_team, agent, potency=i, grey_used=False)
            if score > best_score:
                best_score = score
                best_potency = i
        return best_potency

    if agent == "blue":
        best_score = -math.inf
        best_potency = 0
        grey_used = False
        for i in range(1, 6):
            if i == last_b_potency:
                continue
            score1 = count_sim_score(g_team, agent, potency=i, grey_used=True)
            score2 = count_sim_score(g_team, agent, potency=i, grey_used=False)
            if score1 > score2 and score1 > best_score:
                best_score = score1
                best_potency = i
                grey_used = True
            elif score2 > score1 and score2 > best_score:
                best_score = score2
                best_potency = i
                grey_used = False

        return best_potency, grey_used


main()
