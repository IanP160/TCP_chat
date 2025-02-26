from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def load_routing_table():
    with open("vlan_routing.json", "r") as file:
        return json.load(file)

def save_routing_table(routing_table):
    with open("vlan_routing.json", "w") as file:
        json.dump(routing_table, file, indent=4)

@app.route("/")
def home():
    return render_template("index.html", routing_table=load_routing_table())

@app.route("/update_routing", methods=["POST"])
def update_routing():
    vlan1 = request.form["vlan1"]
    vlan2 = request.form["vlan2"]
    status = request.form["status"] == "true"

    routing_table = load_routing_table()
    routing_table[f"{vlan1}_{vlan2}"] = status
    routing_table[f"{vlan2}_{vlan1}"] = status

    save_routing_table(routing_table)
    return jsonify({"success": True, "message": "Routing updated!"})

if __name__ == "__main__":
    app.run(debug=True)
