import streamlit as st
from streamlit_tree_select import tree_select
import json

st.title("📁 Expandable Org Tree (Simple Python View)")

# Load your nested org chart
uploaded_file = st.file_uploader("Upload org_chart.json", type="json")
if uploaded_file:
    data = json.load(uploaded_file)

    def to_tree_format(node):
        return {
            "label": node["name"],
            "children": [to_tree_format(c) for c in node.get("children", [])]
        }

    tree_data = [to_tree_format(data)]
    selected = tree_select(tree_data)
    st.write("You selected:", selected)
