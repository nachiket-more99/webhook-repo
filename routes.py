from flask import request, jsonify, render_template
from db import events_collection
from dateutil import parser, tz
import requests
from datetime import datetime 

def app_routes(app):
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/webhook", methods=["POST"])
    def webhook():
        event = request.headers.get("X-GitHub-Event")
        data = request.json

        if event == "push":
            dt = parser.isoparse(data["head_commit"]["timestamp"])
            dt_utc = dt.astimezone(tz.UTC) 

            change_obj = {
                "request_id": data["head_commit"]["id"],
                "author": data["head_commit"]["author"]["name"],
                "action": "PUSH",
                "from_branch": None,
                "to_branch": data["ref"].split("/")[-1],
                "timestamp": dt_utc.isoformat()  
            }
            print(change_obj)
            events_collection.insert_one(change_obj)

        elif event == "pull_request":
            pr = data["pull_request"]

            # Fetch user profile to get the name
            user_url = pr["user"]["url"]  
            user_resp = requests.get(user_url)
            user_data = user_resp.json()
            author_name = user_data.get("name") or pr["user"]["login"]  # fallback to login if name is not set

            
            dt = parser.isoparse(pr["created_at"])
            dt_utc = dt.astimezone(tz.UTC)

            change_obj = {
                "request_id": pr["id"],
                "author": author_name,
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": dt_utc.isoformat()
            }
            print(change_obj)
            events_collection.insert_one(change_obj)

        return "", 200

    @app.route("/events", methods=["GET"])
    def get_events():
        events = list(events_collection.find().sort("timestamp", -1))

        for e in events:
            e["_id"] = str(e["_id"])  
            ts = e.get("timestamp")
            if isinstance(ts, str):
                dt = parser.isoparse(ts)
                e["timestamp"] = dt.strftime("%d %B %Y - %I:%M %p UTC")

        return jsonify(events), 200