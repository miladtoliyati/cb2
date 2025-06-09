import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import json
import tempfile

st.set_page_config(page_title="Org Chart", layout="wide")
st.title("📊 Upload Org Chart JSON")

uploaded_file = st.file_uploader("Upload your org_chart.json", type="json")

if uploaded_file is not None:
    data = json.load(uploaded_file)

    def add_nodes_edges(net, node, parent=None):
        name = node["name"]
        net.add_node(name, label=name, title=name)
        if parent:
            net.add_edge(parent, name)
        for child in node.get("children", []):
            add_nodes_edges(net, child, name)

    net = Network(height="750px", width="100%", directed=True)
    net.barnes_hut()
    add_nodes_edges(net, data)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html = open(tmp_file.name, 'r', encoding='utf-8').read()
        components.html(html, height=750, width=1000)
