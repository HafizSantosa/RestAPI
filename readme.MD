## REST API dengan Flask dan MongoDB

### Anggota Kelompok K:
- Muhammad Arsy Athallah - 5027221048 
- Hafiz Akmaldi Santosa - 5027221061
- Almendo Kambu - 5027221073

### Setup Database
```py
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskdb"
mongo = PyMongo(app)
db = mongo.db.items
```
Kami menggunakan flask yang dihubunggkan ke MongoDB dengan PyMongo.

### CRUD
<br>

- Read All
```py
@app.route('/items', methods=['GET'])
def get_items():
    items = []
    for item in db.find():
        items.append({"id": str(item["_id"]), "name": item["name"], "price": item["price"]})
    return jsonify(items)

```
Endpoint: GET http://127.0.0.1:5000/items
<br>

- Read ID
```py
@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = db.find_one({"_id": ObjectId(item_id)})
    if item:
        return jsonify({"id": str(item["_id"]), "name": item["name"], "price": item["price"]})
    return jsonify({"error": "Item not found"}), 404
```
Endpoint: GET http://127.0.0.1:5000/items/[id]
<br>

- Create
```py
@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = {"name": data["name"], "price": data["price"]}
    inserted_item = db.insert_one(new_item)
    return jsonify({"id": str(inserted_item.inserted_id), "name": new_item["name"], "price": new_item["price"]}), 201
```
Endpoint: POST http://127.0.0.1:5000/items
<br>

- Update
```py
@app.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    item = db.find_one({"_id": ObjectId(item_id)})
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.json
    updated_data = {"$set": {"name": data.get("name", item["name"]), "price": data.get("price", item["price"])}}
    db.update_one({"_id": ObjectId(item_id)}, updated_data)
    return jsonify({"id": item_id, "name": data.get("name", item["name"]), "price": data.get("price", item["price"])})
```
Endpoint: PUT http://127.0.0.1:5000/items/[id]
<br>

- Delete
```py
@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = db.find_one({"_id": ObjectId(item_id)})
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.delete_one({"_id": ObjectId(item_id)})
    return jsonify({"message": "Item deleted"})
```
Endpoint: DELETE http://127.0.0.1:5000/items/[id]