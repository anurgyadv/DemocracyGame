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
            node[0], X=random.randint(0, 1), U=round(random.uniform(-1, 1), 1)
        )
    return new_green_team


def visualize_graph(graph):
    """
    This function takes a graph and visualizes it
    """
    new_graph = nx.Graph()
    for node in graph.nodes(data=True):
        color = ""
        if node[1]["X"] == 1:
            color = "blue"
        else:
            color = "red"
        new_graph.add_node(node[0], color=color)

    # Visualize the graph with the X values as the node color, show the edges and the node labels
    nx.draw(
        new_graph,
        node_color=[node[1]["color"] for node in new_graph.nodes(data=True)],
        with_labels=True,
    )
    plt.show()
