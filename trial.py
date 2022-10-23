import csv
import math
import os
import random

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


def blue_interaction(opinion, uncertainty, potency, grey_agent):
    energy = 0
    new_uncertainty = uncertainty
    if opinion == 1:
        if uncertainty - potency / 10 < MINIMUM_UNCERTAINTY:
            new_uncertainty = MINIMUM_UNCERTAINTY
        else:
            new_uncertainty = uncertainty - potency / 10
        if grey_agent != True:
            if uncertainty < 0:
                energy = potency - (uncertainty) * 1.5
            else:
                energy = potency * 1.5

    elif opinion == 0:
        if uncertainty <= -0.5:
            if potency > 3:
                new_uncertainty = uncertainty + 1.12 * potency / 10
            else:
                new_uncertainty = uncertainty + potency / 10

        elif uncertainty >= -0.5 and uncertainty < 0:
            if potency > 3:
                new_uncertainty = uncertainty + 1.34 * potency / 10
            else:
                new_uncertainty = uncertainty + potency / 10
        elif uncertainty >= 0 and uncertainty < 0.5:
            if potency > 3:
                new_uncertainty = uncertainty + 1.56 * potency / 10
            else:
                new_uncertainty = uncertainty + potency / 10
        elif uncertainty > 0.5:
            if potency > 3:
                new_uncertainty = uncertainty - 2 * potency / 10
                opinion = 1
            else:
                if uncertainty + potency / 10 > MAXIMUM_UNCERTAINTY:
                    new_uncertainty = MAXIMUM_UNCERTAINTY
                else:
                    new_uncertainty = uncertainty + potency / 10

        if grey_agent != True:
            energy = potency + uncertainty * 1.5
    return opinion, new_uncertainty, energy


def blue_turn(green_team, chosen_potency, grey=False):
    """_summary_

    Args:
        green_team (_type_): _description_
        chosen_potency (_type_): _description_
        grey (bool, optional): _description_. Defaults to False.

    Work:
        This function simulates the blue turn based on chosen_potency and grey_agent choice
    """
    global blue_energy

    if grey:
        # print("Grey Agent is sending a message to the Green Team, No Energy is used")
        for node in green_team.nodes(data=True):
            # call blue_interaction function
            x, u, f = blue_interaction(
                green_team.nodes[node[0]]["X"],
                green_team.nodes[node[0]]["U"],
                chosen_potency,
                True,
            )
            green_team.nodes[node[0]]["X"] = x
            green_team.nodes[node[0]]["U"] = u
        # print("Grey Agent has sent the message to the Green Team")

    if not grey:
        # print("Blue Agent is sending a message to the Green Team")
        max_loss = 12
        current_used_energy = 0
        # check if grey_agent is spy or not

        for node in green_team.nodes(data=True):
            x, u, energy = blue_interaction(
                green_team.nodes[node[0]]["X"],
                green_team.nodes[node[0]]["U"],
                chosen_potency,
                False,
            )
            green_team.nodes[node[0]]["X"] = x
            green_team.nodes[node[0]]["U"] = u
            current_used_energy += energy / len(green_team.nodes(data=True))
        if current_used_energy > max_loss:
            blue_energy = blue_energy - max_loss
        else:
            blue_energy = blue_energy - current_used_energy


def red_turn(green_team, chosen_potency):

    for node in green_team.nodes(data=True):
        # check if the node is a follower or not
        if not green_team.nodes[node[0]]["F"] == 0:
            # call red_interaction function
            x, u, f = red_interaction(
                green_team.nodes[node[0]]["X"],
                green_team.nodes[node[0]]["U"],
                chosen_potency,
                green_team.nodes[node[0]]["F"],
            )
            green_team.nodes[node[0]]["X"] = x
            green_team.nodes[node[0]]["U"] = u
            green_team.nodes[node[0]]["F"] = f

    return green_team


def red_interaction(opinion, uncertainty, potency, follower):

    if opinion == 1:
        if uncertainty <= -0.5:
            if potency > 3:
                follower = 0
            else:
                uncertainty = uncertainty + potency / 10

        elif uncertainty >= -0.5 and uncertainty < 0:
            if potency > 3:
                follower = 0
            else:
                uncertainty = uncertainty + potency / 10
        elif uncertainty >= 0 and uncertainty < 0.5:
            if potency > 3:
                opinion = 0
                uncertainty = uncertainty - potency / 10 * 1.5
            if potency < 3:
                uncertainty = uncertainty + potency / 10
        elif uncertainty >= 0.5:
            if potency > 3:
                opinion = 0
                uncertainty = -uncertainty
        else:
            uncertainty = uncertainty - potency / 10

    elif opinion == 0:
        if uncertainty <= -0.5:
            if potency > 3:
                opinion = 1
                uncertainty = uncertainty + potency / 10 * 1.5
        else:
            uncertainty = uncertainty + potency / 10
        uncertainty = uncertainty - potency / 10

    return opinion, uncertainty, follower


def start_game(green_team):
    """

    Args:
        green_team (_type_): _description_
    """
    turns = 10
    while turns > 0:
        if not check_game_status():
            temp_red = red_followers
            red_potency = minimax(
                green_team, 0, True, -math.inf, math.inf, 0, agent="red"
            )
            blue_potency, grey = minimax(
                green_team, 0, False, -math.inf, math.inf, 0, agent="blue"
            )

            red_turn(green_team, red_potency)
            blue_turn(green_team, blue_potency, grey)
            green_interaction(green_team)
            blue, red = count_nodes(green_team)
            print(
                "Turn: ",
                turns,
                "Blue Energy: ",
                blue_energy,
                "Red Followers: ",
                temp_red - red_followers,
                "People Voting/ Not Voting ",
                blue,
                "/",
                red,
            )
            turns -= 1
        else:
            end_game(green_team)


def minimax(green_team, depth, isMaximizing, alpha, beta, turn, agent):
    """_summary_

    Args:
        green_team (_type_): _description_
        depth (_type_): _description_
        isMaximizing (_type_): _description_
        alpha (_type_): _description_
        beta (_type_): _description_
        turn (_type_): _description_
        agent (_type_): _description_

    Returns:
        _type_: _description_

    Work:
        If red, finds the best potency with maximum increased people with opinion 0 with minimum followers lost. Returns Potency.
        If blue, finds the best potency with least energy lost and maximum increased people with opinion 1, also determines if using grey_agent is required based on energy. Returns potency and grey = False or True

    """
    if agent == "red":
        if depth == 3:
            return evaluate(green_team, agent)
        if isMaximizing:
            best_potency = -math.inf
            for potency in range(1, 5):
                new_green_team = green_team.copy()
                red_turn(new_green_team, potency)
                value = minimax(
                    new_green_team, depth + 1, False, alpha, beta, turn + 1, agent
                )
                print(best_potency, value)

                best_potency = max(best_potency, value)
                alpha = max(alpha, best_potency)
                if beta <= alpha:
                    break
            return best_potency
        else:
            best_potency = math.inf
            for potency in range(1, 5):
                new_green_team = green_team.copy()
                blue_turn(new_green_team, potency, False)
                value = minimax(
                    new_green_team, depth + 1, True, alpha, beta, turn + 1, agent
                )
                print(best_potency, value)
                best_potency = min(best_potency, value)
                beta = min(beta, best_potency)
                if beta <= alpha:
                    break
            return best_potency
    elif agent == "blue":
        if depth == 3:
            return evaluate(green_team, agent)
        if isMaximizing:
            best_potency = -math.inf
            for potency in range(1, 5):
                new_green_team = green_team.copy()
                grey_ag = False
                blue_turn(new_green_team, potency, grey_ag)
                value, grey_ag = minimax(
                    new_green_team, depth + 1, False, alpha, beta, turn + 1, agent
                )
                print(best_potency, value)

                best_potency = max(best_potency, value)
                alpha = max(alpha, best_potency)
                if beta <= alpha:
                    break
            return best_potency, False
        else:
            best_potency = math.inf
            for potency in range(1, 5):
                grey_ag = True
                new_green_team = green_team.copy()
                blue_turn(new_green_team, potency, grey_ag)
                value, grey_ag = minimax(
                    new_green_team, depth + 1, True, alpha, beta, turn + 1, agent
                )
                print(best_potency, value)

                best_potency = min(best_potency, value)
                beta = min(beta, best_potency)
                if beta <= alpha:
                    break
            return best_potency, True


def evaluate(green_team, agent):
    """_summary_

    Args:
        green_team (_type_): _description_
        agent (_type_): _description_

    Returns:
        _type_: _description_

    Work:
        If red, returns the number of followers lost.
        If blue, returns the number of people with opinion 1.

    """
    if agent == "red":
        followers_lost = 0
        for node in green_team.nodes(data=True):
            if green_team.nodes[node[0]]["F"] == 0:
                followers_lost += 1
        return followers_lost
    elif agent == "blue":
        people_with_opinion_1 = 0
        for node in green_team.nodes(data=True):
            if green_team.nodes[node[0]]["X"] == 1:
                people_with_opinion_1 += 1
        return people_with_opinion_1


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

    # visualize_graph(green_team)

    start_game(green_team)


main()
