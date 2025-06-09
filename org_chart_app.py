import streamlit as st
import json
import uuid
from streamlit_d3_org_chart import d3_org_chart

# Flatten nested org chart to flat list
def flatten_org_chart(data, parent_id=None):
    node_id = str(uuid.uuid4())
    flat = [{
        "id": node_id,
        "parentId": parent_id,
        "name": data["name"]
    }]
    for child in data.get("children", []):
        flat.extend(flatten_org_chart(child, node_id))
    return flat

st.set_page_config(layout="wide")
st.title("📊 Interactive Org Chart (D3 + Expandable + Zoomable)")

uploaded_file = st.file_uploader("Upload your org_chart.json", type="json")

if uploaded_file:
    nested_data = json.load(uploaded_file)
    flat_data = flatten_org_chart(nested_data)

    d3_org_chart(
        data=flat_data,
        id_field="id",
        parent_field="parentId",
        title_field="name",
        width=1000,
        height=800,
        key="org_chart"
    )
