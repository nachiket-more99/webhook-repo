from flask import request, jsonify
from db import events_collection
from dateutil import parser
import requests

def app_routes(app):
    @app.route("/webhook", methods=["POST"])
    def webhook():
        event = request.headers.get("X-GitHub-Event")
        data = request.json

        if event == "push":
            change_obj = {
                "request_id": data["head_commit"]["id"],
                "author": data["head_commit"]["author"]["name"],
                "action": "PUSH",
                "from_branch": None,
                "to_branch": data["ref"].split("/")[-1],
                "timestamp": data["head_commit"]["timestamp"]
            }
            events_collection.insert_one(change_obj)

        elif event == "pull_request":
            pr = data["pull_request"]

            # Fetch user profile to get the name
            user_url = pr["user"]["url"]  
            user_resp = requests.get(user_url)
            user_data = user_resp.json()
            author_name = user_data.get("name") or pr["user"]["login"]  # fallback to login if name is not set

            change_obj = {
                "request_id": pr["id"],
                "author": author_name,
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"]
            }
            events_collection.insert_one(change_obj)

        return "", 200

    @app.route("/events", methods=["GET"])
    def get_events():
        events = events_collection.find().sort("timestamp", -1)

        events_list = []
        for e in events:
            dt = parser.isoparse(e["timestamp"])
            ts = dt.strftime("%d %B %Y - %I:%M %p UTC")

            if e["action"] == "PUSH":
                text = f'{e["author"]} pushed to {e["to_branch"]} on {ts}'
            elif e["action"] == "PULL_REQUEST":
                text = f'{e["author"]} submitted a pull request from {e["from_branch"]} to {e["to_branch"]} on {ts}'
            events_list.append(text)
        return events_list, 200