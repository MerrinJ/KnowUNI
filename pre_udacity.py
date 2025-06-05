import pickle
import networkx as nx
import matplotlib.pyplot as plt
from transformers import BertTokenizer, BertModel
import pandas as pd

with open('bert_model_udacity.pkl', 'rb') as f:
    model = pickle.load(f)

with open('bert_tokenizer_udacity.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def predict_course_description(course_title, data_cleaned):
    description = data_cleaned[data_cleaned['Title'] == course_title]['Description'].iloc[0]
    embedding = get_bert_embeddings(description)
    return embedding

data_cleaned = pd.read_pickle('processed_data_with_embeddings.pkl')

course_to_predict = 'Data Engineering with AWS'
embedding = predict_course_description(course_to_predict, data_cleaned)
print(f"Embedding for {course_to_predict}: {embedding}")

with open('knowledge_graph.gpickle', 'rb') as f:
    knowledge_graph = pickle.load(f)

def draw_graph(graph, title="Knowledge Graph", highlight_nodes=None, highlight_edges=None):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)

    node_colors = []
    for node in graph.nodes(data=True):
        node_type = node[1].get('type', 'unknown')
        if highlight_nodes and node[0] in highlight_nodes:
            node_colors.append('lightgreen')
        elif node_type == 'course':
            node_colors.append('skyblue')
        elif node_type == 'prerequisite':
            node_colors.append('lightgrey')
        else:
            node_colors.append('orange')

    edge_colors = []
    for edge in graph.edges(data=True):
        if highlight_edges and edge in highlight_edges:
            edge_colors.append('red')
        else:
            edge_colors.append('black')

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=1500,
        font_size=10,
        font_weight='bold',
    )

    edge_labels = nx.get_edge_attributes(graph, 'relationship')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='blue')

    legend_labels = {
        'Course': 'skyblue',
        'Prerequisite': 'lightgrey',
        'Highlighted': 'lightgreen',
        'Unknown': 'orange',
    }
    for label, color in legend_labels.items():
        plt.plot([], [], color=color, marker='o', linestyle='', label=label)
    plt.legend(loc='best')

    plt.title(title)
    plt.show()

def visualize_selected_course(graph, course_title, save_path=None):
    subgraph_nodes = list(graph.predecessors(course_title)) + [course_title]
    subgraph = graph.subgraph(subgraph_nodes)

    highlight_nodes = subgraph_nodes
    highlight_edges = [(prereq, course_title) for prereq in graph.predecessors(course_title)]

    prerequisites = list(graph.predecessors(course_title))
    if prerequisites:
        print(f"Prerequisites for {course_title}: {', '.join(prerequisites)}")
    else:
        print(f"There are no prerequisites for {course_title}")

    draw_graph(
        subgraph,
        title=f"Knowledge Graph: {course_title} and its Prerequisites",
        highlight_nodes=highlight_nodes,
        highlight_edges=highlight_edges,
    )

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")

    plt.show()

visualize_selected_course(knowledge_graph, course_to_predict, save_path='course_prerequisites_plot.png')
