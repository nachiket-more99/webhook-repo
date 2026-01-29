from flask import request, jsonify
from db import events_collection

def app_routes(app):
    @app.route("/webhook", methods=["POST"])
    def webhook():
        event = request.headers.get("X-GitHub-Event")
        data = request.json

        if event == "push":
            change_obj = {
                "request_id": data["head_commit"]["id"],
                "author": data["pusher"]["name"],
                "action": "PUSH",
                "from_branch": None,
                "to_branch": data["ref"].split("/")[-1],
                "timestamp": data["head_commit"]["timestamp"]
            }
            events_collection.insert_one(change_obj)

        elif event == "pull_request":
            pr = data["pull_request"]
            change_obj = {
                "request_id": pr["id"],
                "author": pr["user"]["login"],
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"]
            }
            events_collection.insert_one(change_obj)

        return "", 200