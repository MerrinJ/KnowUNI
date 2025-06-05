import networkx as nx
import pickle
import matplotlib.pyplot as plt

with open('knowledge_graph_uiuc.gpickle', 'rb') as f:
    knowledge_graph = pickle.load(f)

def predict_course_prerequisites(course_title, graph):

    prerequisites = list(graph.predecessors(course_title))
    if prerequisites:
        return prerequisites
    else:
        return ["No prerequisites found"]

selected_course = 'AAS 211'
prerequisites = predict_course_prerequisites(selected_course, knowledge_graph)

print(f"Prerequisites for {selected_course}: {', '.join(prerequisites)}")

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

plot_save_path = 'course_prerequisites_plot.png'
plt.savefig(plot_save_path)
print(f"Plot saved to {plot_save_path}")

plt.show()
