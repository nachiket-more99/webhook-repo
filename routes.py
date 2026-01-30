from flask import request, jsonify, render_template
from db import events_collection
from services.github_service import process_push_event, process_pr_event
from utils.formatting import format_event_timestamp


def app_routes(app):
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/webhook", methods=["POST"])
    def webhook():
        event = request.headers.get("X-GitHub-Event")
        data = request.json

        if event == "push":
            process_push_event(data)
        elif event == "pull_request":
            process_pr_event(data)

        return "", 200

    @app.route("/events", methods=["GET"])
    def get_events():
        events = list(events_collection.find().sort("created_at", -1))
        for e in events:
            e["_id"] = str(e["_id"])
            e["timestamp"] = format_event_timestamp(e.get("timestamp"))
        return jsonify(events), 200