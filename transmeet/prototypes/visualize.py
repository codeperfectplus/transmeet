import json

from flask import Flask, render_template_string
from pyvis.network import Network
import json
import uuid

mind_map_path = "mind_map.json"
with open(mind_map_path, 'r') as f:
    mind_map_data = json.load(f)

app = Flask(__name__)

# Function to build the PyVis mindmap
def build_mindmap(data):
    net = Network(height="700px", width="100%", directed=True)
    root_id = "root"
    net.add_node(root_id, label="Mind Map", shape="ellipse", color="#A2D2FF")

    def add_nodes(parent, obj):
        for key, value in obj.items():
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
    return net

@app.route("/")
def index():
    net = build_mindmap(mind_map_data)
    net.save_graph("templates/mindmap.html")

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Mind Map</title></head>
        <body>
            <h2>🧠 Interactive Mind Map</h2>
            <iframe src="/mindmap" width="100%" height="800px" frameborder="0"></iframe>
        </body>
        </html>
    ''')

@app.route("/mindmap")
def mindmap_page():
    return open("templates/mindmap.html", "r").read()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
