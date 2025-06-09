import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import json
import tempfile

st.set_page_config(page_title="Org Chart", layout="wide")
st.title("📊 Interactive Org Chart")

# Load the JSON file bundled with the app
with open("org_chart.json", "r") as f:
    data = json.load(f)

# Recursive function to add nodes and edges
def add_nodes_edges(net, node, parent=None):
    name = node["name"]
    net.add_node(name, label=name, title=name)
    if parent:
        net.add_edge(parent, name)
    for child in node.get("children", []):
        add_nodes_edges(net, child, name)

# Build Pyvis network
net = Network(height="750px", width="100%", directed=True)
net.barnes_hut()
add_nodes_edges(net, data)

# Save and display the network
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp
