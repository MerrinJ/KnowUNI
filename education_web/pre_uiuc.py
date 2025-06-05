import networkx as nx
import pickle
import matplotlib.pyplot as plt

try:
    # Load the knowledge graph
    with open('knowledge_graph_uiuc.gpickle', 'rb') as f:
        knowledge_graph = pickle.load(f)
except FileNotFoundError:
    print("Error: The file 'knowledge_graph_uiuc.gpickle' was not found. Please ensure the file path is correct.")
    knowledge_graph = None
except pickle.UnpicklingError:
    print("Error: The file 'knowledge_graph_uiuc.gpickle' could not be unpickled. Ensure it is a valid gpickle file.")
    knowledge_graph = None


def predict_course_prerequisites(course_title, graph):
    try:
        if graph is None:
            raise ValueError("Knowledge graph is not loaded.")
        prerequisites = list(graph.predecessors(course_title))
        if prerequisites:
            return prerequisites
        else:
            return ["No prerequisites found"]
    except KeyError:
        return ["Error: The course title was not found in the knowledge graph."]
    except ValueError as e:
        return [str(e)]


def plot_knowlegdge(selected_course, prerequisites):
    try:
        if knowledge_graph is None:
            raise ValueError("Knowledge graph is not loaded.")

        subgraph_nodes = [selected_course] + prerequisites
        subgraph = knowledge_graph.subgraph(subgraph_nodes)

        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(subgraph, seed=42)

        nx.draw(
            subgraph,
            pos,
            with_labels=True,
            node_color='lightgreen',
            node_size=2000,
            font_size=10,
            font_weight='bold',
            edge_color='blue'
        )

        plt.title(f"Knowledge Graph: {selected_course} and its Prerequisites")

        plot_save_path = 'education_app/static/plots/course_prerequisites_plot_uiuc.png'
        plt.savefig(plot_save_path)
        print(f"Plot saved to {plot_save_path}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")