import pickle
import networkx as nx
import os
from transformers.activations import GELUActivation  # Import for GELUActivation
from transformers.tokenization_utils import Trie  # Import for Trie

# If BERTProcessor is a custom class, import it
try:
    from your_module import BERTProcessor  # Replace 'your_module' with the actual module
except ImportError:
    BERTProcessor = None  # Set to None if it cannot be imported

# Folder containing pickle files
folder_path = "C:\\Users\\vjnqr\\Downloads\\knowuni(4)\\Devika_full\\education_web"

# Iterate over all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".pkl"):  # Process only .pkl files
        file_path = os.path.join(folder_path, file_name)
        try:
            print(f"Processing {file_name}...")

            # Load the pickle file with additional globals
            with open(file_path, "rb") as f:
                old_data = pickle.load(f, encoding='latin1')

            # Save the fixed pickle file
            with open(file_path, "wb") as f:
                pickle.dump(old_data, f)

            print(f"Fixed and saved: {file_name}")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

print("All pickle files processed.")
