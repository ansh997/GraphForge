import pickle
import networkx as nx
import string


graph_path = './path_graph.pkl'


node_to_name = {
    0: "James", 1: "Robert", 2: "John", 3: "Michael", 4: "David",
    5: "Mary", 6: "Patricia", 7: "Jennifer", 8: "Linda", 9: "Barbara",
    10: "Elizabeth", 11: "Susan", 12: "Jessica", 13: "Sarah", 14: "Karen",
    15: "Nancy", 16: "Margaret", 17: "Lisa", 18: "Betty", 19: "Dorothy"
}

node_to_politician = {
    0: "Barack", 1: "Jimmy", 2: "Arnold", 3: "Bernie", 4: "Bill",
    5: "Kamala", 6: "Hillary", 7: "Elizabeth", 8: "John", 9: "Joe",
    10: "Donald", 11: "George", 12: "Ronald", 13: "Richard", 14: "Lyndon",
    15: "Gerald", 16: "Theodore", 17: "Franklin", 18: "Harry", 19: "Dwight"
}

def adjacency(G):
    all_nodes = list(G.nodes())  # Get all nodes directly from G
    adjacency_list = G.edges()
    adj_list = ", ".join(f"({u}, {v})" for u, v in adjacency_list)  # Formatting change for clarity

    encoding = f"In an undirected graph, (i, j) means that node i and node j are connected with an undirected edge. G describes a graph among nodes {all_nodes}. The edges in G are: {adj_list}."
    print(encoding)
    return encoding


def incident(G):
    description = "G describes a graph among " + ", ".join(map(str, G.nodes)) + ".\nIn this graph:"
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        if len(neighbors) == 1:
            description += f"\nNode {node} is connected to node {neighbors[0]}."
        else:
            description += f"\nNode {node} is connected to nodes {', '.join(map(str, neighbors[:-1]))}, {neighbors[-1]}."

    print(description, G.edges)        
    return description

def co_authorship(G):
    authors = ", ".join([node_to_name[node] for node in G.nodes])
    description = f"G describes a co-authorship graph among {authors}.\nIn this co-authorship graph:"
    for edge in G.edges():
        author1, author2 = node_to_name[edge[0]], node_to_name[edge[1]]
        description += f"\n{author1} and {author2} wrote a paper together."

    print(description)    
    return description


def friendship(G):
    friends = ", ".join([node_to_name[node] for node in G.nodes])
    description = f"G describes a friendship graph among {friends}.\nWe have the following edges in G:"
    for edge in G.edges():
        friend1, friend2 = node_to_name[edge[0]], node_to_name[edge[1]]
        description += f"\n{friend1} and {friend2} are friends."
    print(description)    
    return description

def social_network(G):
    names = [node_to_name[node] for node in G.nodes]
    intro = f"G describes a social network graph among {', '.join(names)}.\nWe have the following edges in G:"
    
    connections = []
    for edge in G.edges():
        name1, name2 = node_to_name[edge[0]], node_to_name[edge[1]]
        connections.append(f"{name1} and {name2} are connected.")
    
    description = intro + "\n" + "\n".join(connections)

    print(description)
    return description

def polotician(G):
    friends = ", ".join([node_to_name[node] for node in G.nodes])
    description = f"G describes a friendship graph among {friends}.\nWe have the following edges in G:"
    for edge in G.edges():
        friend1, friend2 = node_to_name[edge[0]], node_to_name[edge[1]]
        description += f"\n{friend1} and {friend2} are friends."

    print(description)    
    return description

def expert(G):
    # Mapping from node numbers to expert labels (A, B, C, ...)
    node_to_label = {i: label for i, label in enumerate(string.ascii_uppercase[:20])}  # Supports up to 20 nodes

    # Start the description with an introductory sentence
    labels = [node_to_label[node] for node in G.nodes]
    intro = f"You are a graph analyst and you have been given a graph G among {', '.join(labels)}. G has the following undirected edges:"

    # Iterate over each edge to describe the connections
    connections = []
    for edge in G.edges():
        label1, label2 = node_to_label[edge[0]], node_to_label[edge[1]]
        connections.append(f"{label1} -> {label2}")

    # Combine the introduction and all connection descriptions
    description = intro + "\n" + "\n".join(connections)
    print(description)
    return description

    

with open('./path_graph.pkl', 'rb') as f:
    pg = pickle.load(f)

    
adjacency(pg)    



    

