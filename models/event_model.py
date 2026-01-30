from datetime import datetime, timezone

def build_event(data):
    ts = data.get("timestamp")
    if ts:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        ts_utc = dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        ts_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "request_id": str(data["request_id"]),
        "author": data["author"],
        "action": data["action"],
        "from_branch": data.get("from_branch"),
        "to_branch": data.get("to_branch"),
        "timestamp": ts_utc,
        "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }