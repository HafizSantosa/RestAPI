from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy
items = [
    {"id": 1, "name": "Sepatu", "price": 10.0},
    {"id": 2, "name": "Sandal", "price": 20.0}
]

# Read all
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Read ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# Create
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    new_item["id"] = len(items) + 1
    items.append(new_item)
    return jsonify(new_item), 201

# Update
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.json
    item.update(data)
    return jsonify(item)

# Delete
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(debug=True)

#Endpoints
# GET /items

# GET /items/<id>

# POST /items
# {
#     "name": "Item 3",
#     "price": 30.0
# }

# PUT /items/<id>
# {
#     "name": "Updated Item 1",
#     "price": 15.0
# }

# DELETE /items/<id>

