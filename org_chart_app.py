import streamlit as st
from pyvis.network import Network
import json
import tempfile
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("📊 Org Chart (Pyvis Top-Down Layout)")

uploaded_file = st.file_uploader("Upload your org_chart.json", type="json")
if uploaded_file:
    data = json.load(uploaded_file)

    def add_nodes_edges(net, node, parent=None):
        net.add_node(node["name"], label=node["name"])
        if parent:
            net.add_edge(parent, node["name"])
        for child in node.get("children", []):
            add_nodes_edges(net, child, node["name"])

    net = Network(height="750px", width="100%", directed=True)
    net.set_options(json.dumps({
        "layout": {
            "hierarchical": {
                "enabled": True,
                "direction": "UD",
                "sortMethod": "directed"
            }
        },
        "physics": {
            "hierarchicalRepulsion": {
                "centralGravity": 0.0,
                "springLength": 100,
                "springConstant": 0.01,
                "nodeDistance": 120,
                "damping": 0.09
            },
            "solver": "hierarchicalRepulsion"
        }
    }))

    add_nodes_edges(net, data)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        path = tmp_file.name
        net.save_graph(path)
        html = open(path, 'r', encoding='utf-8').read()
        components.html(html, height=800, scrolling=True)
