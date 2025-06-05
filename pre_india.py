import networkx as nx
import matplotlib.pyplot as plt
import pickle

with open("knowledge_graph_india.gpickle", "rb") as f:
    knowledge_graph = pickle.load(f)

def display_single_course_graph(course_name):
    if course_name in knowledge_graph.nodes:
        subgraph_nodes = list(knowledge_graph.predecessors(course_name)) + [course_name]
        subgraph = knowledge_graph.subgraph(subgraph_nodes)

        plt.figure(figsize=(8, 4))
        pos = nx.spring_layout(subgraph, seed=42)
        nx.draw(
            subgraph,
            pos,
            with_labels=True,
            node_color='lightgreen',
            node_size=1500,
            font_size=10,
            font_weight='bold',
        )
        plt.title(f"Knowledge Graph: {course_name} and its Subject Combinations")

        plot_save_path = f"{course_name}_subject_combinations.png"
        plt.savefig(plot_save_path)
        print(f"Plot saved to {plot_save_path}")
        plt.show()
    else:
        print(f"Course '{course_name}' not found in the knowledge graph.")

