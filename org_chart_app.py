import streamlit as st
import json
import uuid
import streamlit.components.v1 as components
import tempfile
import os

# Flatten nested org chart into D3-compatible structure
def flatten_org_chart(data, parent_id=None):
    node_id = str(uuid.uuid4())
    flat_list = [{
        "id": node_id,
        "parentId": parent_id,
        "name": data["name"],
    }]
    for child in data.get("children", []):
        flat_list.extend(flatten_org_chart(child, node_id))
    return flat_list

st.set_page_config(layout="wide")
st.title("📊 Interactive Org Chart (Zoomable + Expandable)")

uploaded_file = st.file_uploader("Upload your org_chart.json", type="json")

if uploaded_file:
    raw_data = json.load(uploaded_file)
    flat_data = flatten_org_chart(raw_data)
    data_json = json.dumps(flat_data).replace("</", "<\\/")

    html_template = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          html, body, #chart {{
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            font-family: Arial, sans-serif;
          }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
        <script src="https://cdn.jsdelivr.net/npm/d3-org-chart@3.1.3"></script>
      </head>
      <body>
        <div id="chart"></div>
        <script>
          const data = {data_json};
          const chart = new d3.OrgChart()
            .container("#chart")
            .data(data)
            .nodeHeight(d => 80)
            .nodeWidth(d => 250)
            .childrenMargin(d => 40)
            .compactMarginBetween(d => 15)
            .compactMarginPair(d => 30)
            .nodeContent(d => `
              <div style="padding:10px;border:1px solid #ccc;border-radius:4px;background:#fff;">
                <div style="font-weight:bold;">\${{d.data.name}}</div>
              </div>
            `)
            .render();
        </script>
      </body>
    </html>
    """

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding="utf-8") as f:
        f.write(html_template)
        temp_path = f.name

    components.iframe(f"file://{temp_path}", height=800, scrolling=True)
