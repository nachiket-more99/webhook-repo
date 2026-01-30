from db import events_collection
from dateutil import parser, tz
import requests
from datetime import datetime
from models.event_model import build_event

def process_push_event(data):
    branch = data["ref"].split("/")[-1]
    dt = parser.isoparse(data["head_commit"]["timestamp"])
    dt_utc = dt.astimezone(tz.UTC)

    change_obj = build_event({
        "request_id": data["head_commit"]["id"],
        "author": data["head_commit"]["author"]["name"],
        "action": "PUSH",
        "from_branch": branch,
        "to_branch": branch,
        "timestamp": dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    events_collection.insert_one(change_obj)

def process_pr_event(data):
    pr = data["pull_request"]
    user_resp = requests.get(pr["user"]["url"])
    user_data = user_resp.json()
    author_name = user_data.get("name") or pr["user"]["login"]

    dt = parser.isoparse(pr["created_at"])
    dt_utc = dt.astimezone(tz.UTC)

    change_obj = build_event({
        "request_id": str(pr["id"]),
        "author": author_name,
        "action": "PULL_REQUEST",
        "from_branch": pr["head"]["ref"],
        "to_branch": pr["base"]["ref"],
        "timestamp": dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    events_collection.insert_one(change_obj)