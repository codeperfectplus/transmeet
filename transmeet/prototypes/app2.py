import uuid
import json
from flask import Flask, Response
from pyvis.network import Network

# Constants
MIND_MAP_PATH = "mind_map.json"

# Load mind map data
def load_mind_map_data(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading mind map data: {e}")
        return {}

app = Flask(__name__)
mind_map_data = load_mind_map_data(MIND_MAP_PATH)

# Build PyVis mind map and return HTML string
def build_mindmap_html(data):
    net = Network(height="750px", width="100%", bgcolor="#fff", font_color="black")
    root_id = "root"
    net.add_node(root_id, label=data.get("Root Topic", "Mind Map"), shape="ellipse", color="#A2D2FF")
    # del data["Root Topic"]  # Remove root topic from data if it exists

    def add_nodes(parent, obj):
        for key, value in obj.items():
            if key == "Root Topic":
                continue
            node_id = str(uuid.uuid4())
            net.add_node(node_id, label=key, shape="box", color="#FFAFCC")
            net.add_edge(parent, node_id)

            if isinstance(value, dict):
                add_nodes(node_id, value)
            elif isinstance(value, list):
                for item in value:
                    leaf_id = str(uuid.uuid4())
                    net.add_node(leaf_id, label=item, shape="text", color="#BDB2FF")
                    net.add_edge(node_id, leaf_id)

    add_nodes(root_id, data)
    net.repulsion(node_distance=120)
    net.show_buttons(filter_=['physics'])
    return net.generate_html()

@app.route("/")
def index():
    html_content = build_mindmap_html(mind_map_data)
    return Response(html_content, mimetype='text/html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
