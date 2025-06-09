import streamlit as st
from streamlit_echarts import st_echarts
import json
import uuid

st.set_page_config(layout="wide")
st.title("📊 Interactive Org Chart (ECharts Force Graph)")

uploaded_file = st.file_uploader("Upload your org_chart.json", type="json")
if uploaded_file:
    raw_data = json.load(uploaded_file)

    # Flatten to ECharts format
    def flatten_to_nodes_links(node, parent=None, nodes=None, links=None):
        if nodes is None: nodes = []
        if links is None: links = []

        node_id = str(uuid.uuid4())
        nodes.append({"id": node_id, "name": node["name"]})
        if parent:
            links.append({"source": parent, "target": node_id})

        for child in node.get("children", []):
            flatten_to_nodes_links(child, node_id, nodes, links)

        return nodes, links

    nodes, links = flatten_to_nodes_links(raw_data)

    option = {
        "tooltip": {},
        "series": [{
            "type": "graph",
            "layout": "force",
            "roam": True,
            "label": {
                "show": True
            },
            "edgeSymbol": ["circle", "arrow"],
            "edgeSymbolSize": [4, 10],
            "edgeLabel": {
                "fontSize": 10
            },
            "data": nodes,
            "links": links,
            "lineStyle": {
                "opacity": 0.9,
                "width": 1,
                "curveness": 0.2
            },
            "force": {
                "repulsion": 300,
                "edgeLength": 120
            }
        }]
    }

    st_echarts(options=option, height="700px")
