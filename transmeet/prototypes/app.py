# cython: language_level=3
from flask import Flask, render_template, request, jsonify
import uuid
import json
import os
from datetime import datetime

app = Flask(__name__)

def generate_id():
    """Generate a short UUID for node identification"""
    return str(uuid.uuid4())[:8]

def load_mindmap(file_path):
    """Load mind map data from JSON file with error handling"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Mind map file not found: {file_path}")
            # Return a default empty mind map
            return {"Root Topic": "New Mind Map"}
    except Exception as e:
        print(f"Error loading mind map data: {e}")
        return {"Root Topic": "Error Loading Mind Map"}

def convert_to_jsmind(data):
    """Convert dictionary data structure to jsMind format with metadata and styling"""
    root_id = generate_id()
    
    # Create the base jsMind structure
    jsmind = {
        "meta": {
            "name": data.get("Root Topic", "Mind Map"),
            "author": "Mind Map Creator",
            "version": "1.0",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "format": "node_array",
        "data": [
            {
                "id": root_id, 
                "isroot": True, 
                "topic": data.get("Root Topic", "Mind Map"),
                "direction": "right",
                "expanded": True,
                "background-color": "#2563eb",
                "foreground-color": "#ffffff"
            }
        ]
    }
    
    # Colors for different levels
    level_colors = [
        {"bg": "#06b6d4", "fg": "#ffffff"},  # Level 1
        {"bg": "#0ea5e9", "fg": "#ffffff"},  # Level 2
        {"bg": "#3b82f6", "fg": "#ffffff"},  # Level 3
        {"bg": "#6366f1", "fg": "#ffffff"},  # Level 4
        {"bg": "#8b5cf6", "fg": "#ffffff"},  # Level 5
    ]
    
    def add_nodes(parent_id, children, level=0):
        """Recursively add nodes to the jsMind structure with styling based on level"""
        if not isinstance(children, dict):
            return
        
        for k, v in children.items():
            if k == "Root Topic":
                continue
                
            child_id = generate_id()
            color_index = min(level, len(level_colors)-1)
            
            # Create node with styling
            node = {
                "id": child_id, 
                "parentid": parent_id, 
                "topic": k,
                "expanded": False,  # Default to collapsed
                "background-color": level_colors[color_index]["bg"],
                "foreground-color": level_colors[color_index]["fg"]
            }
            
            # Add direction to first-level nodes
            if level == 0:
                # Alternate left/right for better layout
                direction = "right" if len(jsmind["data"]) % 2 == 0 else "left"
                node["direction"] = direction
                
            jsmind["data"].append(node)
            
            if isinstance(v, dict):
                add_nodes(child_id, v, level + 1)
            elif isinstance(v, list):
                for item in v:
                    leaf_id = generate_id()
                    leaf_color_index = min(level + 1, len(level_colors)-1)
                    jsmind["data"].append({
                        "id": leaf_id, 
                        "parentid": child_id, 
                        "topic": item,
                        "background-color": level_colors[leaf_color_index]["bg"],
                        "foreground-color": level_colors[leaf_color_index]["fg"]
                    })
    
    add_nodes(root_id, data)
    return jsmind

# Routes
@app.route("/")
def index():
    """Main page route"""
    # Load and convert mind map data
    mindmap_dict = load_mindmap("mind_map.json")
    jsmind_data = convert_to_jsmind(mindmap_dict)
    
    # For debugging
    app.logger.debug(f"Generated jsMind data with {len(jsmind_data['data'])} nodes")
    
    return render_template("index.html", 
                           jsmind_data=json.dumps(jsmind_data),
                           map_title=mindmap_dict.get("Root Topic", "Mind Map"))


# Error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, port=5002)
