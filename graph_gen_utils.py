import networkx as nx
import datetime
import os
import random
import matplotlib.pyplot as plt
from graph_encoding import node_to_name, node_to_politician, node_to_GoT_characters, node_to_sp_characters, expert

graph_encodings = {
    "Adjacency": {
        "node_encoding": "integer",
        "edge_encoding": "parenthesis"
    },
    "Incident": {
        "node_encoding": "integer",
        "edge_encoding": "incident"
    },
    "Friendship": {
        "node_encoding": "well-known English first names",
        "edge_encoding": "friendship"
    },
    "Co-authorship": {
        "node_encoding": "well-known English first names",
        "edge_encoding": "coauthorship"
    },
    "SP": {
        "node_encoding": "South Park character names",
        "edge_encoding": "friendship"
    },
    "GOT": {
        "node_encoding": "Game of Thrones character names",
        "edge_encoding": "friendship"
    },
    "Social network": {
        "node_encoding": "well-known English first names",
        "edge_encoding": "social network"
    },
    "Politician": {
        "node_encoding": "American politician first names",
        "edge_encoding": "social network"
    },
    "Expert": {
        "node_encoding": "Alphabet",
        "edge_encoding": "arrows"
    }
}

lists_for_node_encoding = {'Friendship': list(node_to_name.values()),
                           'GOT': node_to_GoT_characters,
                           'SP': node_to_sp_characters,
                           'Politician': list(node_to_politician.values()),
                           'Co-authorship': list(node_to_name.values()),
                           'Social network': list(node_to_name.values())}

def generate_graph(graph_type: str, nodes: int=None, directed: bool=False):
    """Helper function to generate graphs

    Args:
        graph_type (str): Choose a valid Graph type from ER, BA, SBM, SFN, Path, Star, Complete
        nodes (int, optional): Choose number of nodes in the graph. Defaults to None.
        directed (bool, optional): Flag for generating directed graphs. Defaults to False.

    Raises:
        ValueError: Invalid Graph type

    Returns:
        NetworkX graph object: Graph
    """
    if nodes is None:
        nodes = random.randint(5, 20)
    
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    if graph_type.upper() == 'ER':
        p = random.uniform(0, 1)
        G = nx.erdos_renyi_graph(nodes, p, directed=directed)
    elif graph_type.upper() == 'BA':
        m = random.randint(1, nodes)
        G = nx.barabasi_albert_graph(nodes, m, directed=directed)
    elif graph_type.upper() == 'SBM':
        communities = random.randint(2, 10)
        G = nx.stochastic_blockmodel_graph([nodes]*communities, [[0.5]*communities]*communities, directed=directed)
    elif graph_type.upper() == 'SFN':
        G = nx.scale_free_graph(nodes, directed=directed)
    elif graph_type.upper() == 'Path':
        G = nx.path_graph(nodes, directed=directed)
    elif graph_type == 'Star':
        G = nx.star_graph(nodes, directed=directed)
    elif graph_type == 'Complete':
        G = nx.complete_graph(nodes, directed=directed)
    else:
        raise ValueError("Invalid graph type")
    
    return G


def draw_graph(G):
    """Plot Graph

    Args:
        G (NetworkX graph object): Graph to plot
    """
    plt.figure(figsize=(8, 8))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=500, font_size=10, font_weight='bold')
    plt.show()


def edge_encoding(graph, encoding_type: str='Incident', encoded_nodes: list=None):
    if encoding_type.title() not in "Parenthesis, Friendship, Coauthorship, Social Network, Arrows, Incident".split(', '):
        raise ValueError("Invalid encoding {encoding_type}")
    
    encoded_graph = {}
    if encoded_nodes is None:
        encoded_nodes = {node: node for node in graph.nodes()}
    
    if encoding_type.title() == 'Parenthesis':
        for edge in graph.edges():
            encoded_graph[edge] = f"({encoded_nodes[edge[0]]}, {encoded_nodes[edge[1]]})"
    elif encoding_type.title() == 'Friendship':
        for edge in graph.edges():
            encoded_graph[edge] = f"{encoded_nodes[edge[0]]} and {encoded_nodes[edge[1]]} are friends."
    elif encoding_type.title() == 'Coauthorship':
        for edge in graph.edges():
            encoded_graph[edge] = f"{encoded_nodes[edge[0]]} and {encoded_nodes[edge[1]]} wrote a paper together."
    elif encoding_type.title() == 'Social Network':
        for edge in graph.edges():
            encoded_graph[edge] = f"{encoded_nodes[edge[0]]} and {encoded_nodes[edge[1]]} are connected."
    elif encoding_type.title() == 'Arrows':
        for edge in graph.edges():
            encoded_graph[edge] = f"{encoded_nodes[edge[0]]} -→ {encoded_nodes[edge[1]]}"
    elif encoding_type.title() == 'Incident':
        for edge in graph.edges():
            for node in graph.nodes():
                neighbors = list(graph.neighbors(node))
                encoded_graph[node] = neighbors
    else:
        raise ValueError("Invalid encoding type")
    
    return encoded_graph


def node_encoding(graph, encoding_type: str, list_of_encoded_nodes: list = None):
    """
    Encodes the nodes of a graph based on the specified encoding type.
    
    Parameters:
    - graph: The NetworkX graph object.
    - encoding_type: The type of encoding to apply.
    - list_of_encoded_nodes: A list of encoded node names or characters. Required for encoding types other than 'Integer'.
    
    Returns:
    - A dictionary where keys are original node identifiers and values are the encoded node identifiers.
    """
    if 'names' in encoding_type.lower():
        encoding_type = 'EnglishNames'
        
    valid_encodings = ["Integer", "Englishnames", "GoT", "SP", "Alphabet"]
    
    if encoding_type.title() not in valid_encodings:
        raise ValueError("Invalid encoding type. Valid types are: " + ', '.join(valid_encodings))
    
    if encoding_type != 'Integer' and list_of_encoded_nodes is None: # or len(list_of_encoded_nodes) != len(graph.nodes())):
        raise ValueError("For encoding types other than 'Integer', a list of encoded nodes must be provided and match the number of nodes in the graph.")
    
    if encoding_type == 'Integer':
        return {node: f"{node}" for node in graph.nodes()}
    
    print(f"Encoding nodes using {encoding_type}, {list_of_encoded_nodes}")
    
    print('printing...')
    for node in graph.nodes():
        print(list_of_encoded_nodes[node % len(list_of_encoded_nodes)]) 
    print('\t ended')
    
    return {node: list_of_encoded_nodes[node % len(list_of_encoded_nodes)] for node in graph.nodes()}


def graph_encoding(graph, node_encoding_type, edge_encoding_type, list_of_encoded_nodes=None):
    """
    Encodes a graph using specified node and edge encoding types.
    
    Parameters:
    - graph: The NetworkX graph object.
    - node_encoding_type: The type of node encoding to apply.
    - edge_encoding_type: The type of edge encoding to apply.
    
    Returns:
    - A string describing the graph according to the specified encodings.
    """
    encoded_nodes = node_encoding(graph, node_encoding_type, list_of_encoded_nodes)
    print(f'{encoded_nodes=}')
    
    encoded_edges   = edge_encoding(graph, edge_encoding_type, encoded_nodes)
    description = f"{edge_encoding_type}: G describes a {edge_encoding_type.lower()} graph among {', '.join(encoded_nodes.values())}.\n"
    if edge_encoding_type.title() == 'Incident':
        description += f"In this graph:"
        for node, neighbors in graph.adjacency():
            description += f"Node {encoded_nodes[node]} is connected to nodes {', '.join(encoded_nodes[n] for n in neighbors)}.\n"
    elif edge_encoding_type.title() == 'Expert':
        description = expert(graph)
    else:
        description += "The edges in G are:\n"
        for _, encoded_edge in encoded_edges.items():
            description += f"{encoded_edge}\n"
    return description


def gen_save_graphs(graph_type: str, nodes: int=None, directed: bool=False, save_path: str=None, filename:str=None):
    G = generate_graph(graph_type, nodes, directed)
    dir_flag = 'undirected' if not directed else 'directed'
    
    save_path = os.path.join(os.getcwd(), 'data', graph_type) if \
        save_path is None else os.path.join(save_path, 'data', graph_type)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filename = f"{graph_type}_{nodes}_{dir_flag}_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.gpickle" if filename is None else filename
    save_path = os.path.join(save_path, filename)
    nx.write_gpickle(G, save_path)
    print(f"Saved {graph_type} graph to {save_path}")
    return G


def load_graph_from_path(path):
    """
    Loads a graph from a specified path.
    
    Parameters:
    - path: The path to the file where the graph is saved.
    
    Returns:
    - The loaded graph object.
    """
    return nx.read_gpickle(path)


def encode_graph(graph, encoding_type, list_of_encoded_nodes=None):
    """_summary_

    Args:
        graph (_type_): _description_
        encoding_type (_type_): _description_
        list_of_encoded_nodes (_type_, optional): _description_. Defaults to None.
    """
    if encoding_type.title() == 'Expert':
        return expert(graph)
    node_encoding_type, edge_encoding_type = [s.title() for s in graph_encodings[encoding_type].values()]
    print(f"Encoding type: {encoding_type}, {node_encoding_type=}, {edge_encoding_type=}")
    if node_encoding_type.title() not in ['Integer']:
        list_of_encoded_nodes = lists_for_node_encoding[encoding_type] if list_of_encoded_nodes is None else list_of_encoded_nodes
    # list_of_encoded_nodes = list_of_encoded_nodes[:len(graph.nodes())]
    desc = graph_encoding(graph, node_encoding_type, edge_encoding_type, list_of_encoded_nodes)
    return desc


if __name__ == '__main__':
    #  Example usage
    graph_type = 'ER' # Change this to any of the supported types
    graph = generate_graph(graph_type)
    # draw_graph(graph)

    print(edge_encoding(graph, 'Parenthesis'))

    print(node_encoding(graph, 'Integer'))

    print(encode_graph(graph, 'Adjacency'))
    print(encode_graph(graph, 'Politician'))
    print(encode_graph(graph, 'Incident'))
    print(encode_graph(graph, 'Friendship'))
    print(encode_graph(graph, 'Co-authorship'))
    print(encode_graph(graph, 'SP'))
    print(encode_graph(graph, 'GOT'))
    print(encode_graph(graph, 'Social network'))
    print(encode_graph(graph, 'Politician'))
    print(encode_graph(graph, 'Expert'))
    
    
    
    
    
    
    
    
    
    

    
    