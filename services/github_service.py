from db import events_collection
from dateutil import parser, tz
import requests
from datetime import datetime, timezone
from models.event_model import build_event

def process_push_event(data):
    head_commit = data.get("head_commit")
    if not head_commit:
        return

    msg = head_commit.get("message", "")

    if (
        msg.startswith("Merge pull request")
        or msg.startswith("Merge branch")
    ):
        return

    dt = parser.isoparse(data["head_commit"]["timestamp"])
    dt_utc = dt.astimezone(tz.UTC)

    change_obj = build_event({
        "request_id": head_commit["id"],
        "author": head_commit["author"]["name"],
        "action": "PUSH",
        "from_branch": None,
        "to_branch": data["ref"].split("/")[-1],
        "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })

    events_collection.insert_one(change_obj)


def process_pr_event(data):
    pr = data["pull_request"]
    action = data.get("action")

    if action not in ("opened", "closed"):
        return

    if action == "synchronize":
        return

    user_resp = requests.get(pr["user"]["url"])
    user_data = user_resp.json()
    author_name = user_data.get("name") or pr["user"]["login"]

    print("Action: ", action)

    if action == "closed" and pr.get("merged"):
        dt = parser.isoparse(pr["merged_at"]).astimezone(tz.UTC)
        action_type = "MERGE"

    elif action == "opened":
        dt = parser.isoparse(pr["created_at"]).astimezone(tz.UTC)
        action_type = "PULL_REQUEST"

    else:
        return

    change_obj = build_event({
        "request_id": str(pr["id"]),
        "author": author_name,
        "action": action_type,
        "from_branch": pr["head"]["ref"],
        "to_branch": pr["base"]["ref"],
        "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    events_collection.insert_one(change_obj)