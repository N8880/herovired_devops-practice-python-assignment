"""
Q3 (continued): Simple Flask API exposing the parsed configuration data.

Run config_parser.py first to generate config_data.json, then start this
API and issue a GET request to fetch it:

    python config_parser.py
    python api.py

    curl http://127.0.0.1:5000/config
    curl http://127.0.0.1:5000/config/Database
"""

import json
import os

from flask import Flask, jsonify

DATA_FILE = "config_data.json"

app = Flask(__name__)


def load_data() -> dict:
    if not os.path.isfile(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


@app.route("/config", methods=["GET"])
def get_all_config():
    """Return the full parsed configuration as JSON."""
    data = load_data()
    if not data:
        return jsonify({"error": f"No data found. Run config_parser.py first to generate {DATA_FILE}."}), 404
    return jsonify(data), 200


@app.route("/config/<section>", methods=["GET"])
def get_section(section):
    """Return a single section (e.g. /config/Database) as JSON."""
    data = load_data()
    if section not in data:
        return jsonify({"error": f"Section '{section}' not found."}), 404
    return jsonify({section: data[section]}), 200


if __name__ == "__main__":
    app.run(debug=True)
