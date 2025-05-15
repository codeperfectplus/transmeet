import uuid
import json
from flask import Flask, render_template, jsonify

# Generate a short unique ID for each node
def generate_id():
    return str(uuid.uuid4())[:8]

# Convert nested dict/list data to jsmind compatible JSON
def convert_to_jsmind(data):
    root_id = generate_id()
    jsmind = {
        "meta": {
            "name": "AI Mind Map",
            "author": "Your Name",
            "version": "1.0"
        },
        "format": "node_array",
        "data": [
            {"id": root_id, "isroot": True, "topic": "AI in Actuarial and Finance"}
        ]
    }

    def add_nodes(parent_id, children):
        if not isinstance(children, dict):
            return
        for k, v in children.items():
            child_id = generate_id()
            jsmind["data"].append({"id": child_id, "parentid": parent_id, "topic": k})
            if isinstance(v, dict):
                add_nodes(child_id, v)
            elif isinstance(v, list):
                for item in v:
                    leaf_id = generate_id()
                    jsmind["data"].append({"id": leaf_id, "parentid": child_id, "topic": item})

    add_nodes(root_id, data)
    return jsmind

# Load mind map data from JSON file safely
def load_mindmap(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading mind map data: {e}")
        return {}

# Initialize Flask app
app = Flask(__name__)

# Load data once at startup
mindmap_dict = load_mindmap("mind_map.json")

@app.route("/")
def index():
    # Ensure you have a templates/index.html file for this to render properly
    return render_template("index.html")

@app.route("/mindmap_data")
def get_mindmap_data():
    # Convert dict to jsmind JSON and return as response
    jsmind_data = convert_to_jsmind(mindmap_dict)
    return jsonify(jsmind_data)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
