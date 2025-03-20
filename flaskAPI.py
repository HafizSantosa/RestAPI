from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskdb"
mongo = PyMongo(app)
db = mongo.db.items

# GET ALL
@app.route('/items', methods=['GET'])
def get_items():
    items = []
    for item in db.find():
        items.append({"id": str(item["_id"]), "name": item["name"], "price": item["price"]})
    return jsonify(items)

# GET ID
@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = db.find_one({"_id": ObjectId(item_id)})
    if item:
        return jsonify({"id": str(item["_id"]), "name": item["name"], "price": item["price"]})
    return jsonify({"error": "Item not found"}), 404

# POST
@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = {"name": data["name"], "price": data["price"]}
    inserted_item = db.insert_one(new_item)
    return jsonify({"id": str(inserted_item.inserted_id), "name": new_item["name"], "price": new_item["price"]}), 201

# PUT
@app.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    item = db.find_one({"_id": ObjectId(item_id)})
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.json
    updated_data = {"$set": {"name": data.get("name", item["name"]), "price": data.get("price", item["price"])}}
    db.update_one({"_id": ObjectId(item_id)}, updated_data)
    return jsonify({"id": item_id, "name": data.get("name", item["name"]), "price": data.get("price", item["price"])})

# DELETE
@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = db.find_one({"_id": ObjectId(item_id)})
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.delete_one({"_id": ObjectId(item_id)})
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

