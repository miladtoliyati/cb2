import streamlit as st
import json
import uuid
import streamlit.components.v1 as components

# Convert nested org chart to flat list with id, parentId
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

# Upload JSON
st.set_page_config(layout="wide")
st.title("📊 Interactive Org Chart (Zoomable + Expandable)")

uploaded_file = st.file_uploader("Upload your org_chart.json", type="json")
if uploaded_file is not None:
    raw_data = json.load(uploaded_file)
    flat_data = flatten_org_chart(raw_data)

    data_json = json.dumps(flat_data)

    # Inject the HTML+JS for D3 org chart
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <script src="https://d3js.org/d3.v6.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/d3-org-chart@3.1.3"></script>
    </head>
    <body>
      <div id="chart"></div>
      <script>
        const data = {data_json};
        const chart = new d3.OrgChart()
          .container("#chart")
          .data(data)
          .nodeHeight((d) => 80)
          .childrenMargin((d) => 40)
          .compactMarginBetween((d) => 35)
          .compactMarginPair((d) => 30)
          .nodeContent((d, i, arr, state) => `
            <div style='padding:10px;background:#ffffff;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,0.1);'>
              <div style='font-weight:bold;font-size:14px;'>${d.data.name}</div>
            </div>
          `)
          .render();
      </script>
    </body>
    </html>
    """

    components.html(html_code, height=800, scrolling=True)
