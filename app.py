# app.py

from flask import Flask, request, jsonify, render_template
import json
from tracker import track_deals

app = Flask(__name__)

CONFIG_FILE = "config.json"

@app.route("/")
def home():
    return render_template("myra_ui.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    try:
        product_entry = {
            "name": data["name"],
            "min_price": int(data["min_price"]),
            "max_price": int(data["max_price"]),
            "sites": data.get("sites", ["Amazon", "Flipkart", "Myntra"])
        }

        # Load existing config
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        config["products"].append(product_entry)

        # Save updated config
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

        # Trigger the tracker
        track_deals()

        return jsonify({"status": "success", "message": "Tracking started!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
