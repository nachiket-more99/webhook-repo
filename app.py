from flask import Flask, request, json

app = Flask(__name__)

@app.route("/")
def health():
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.headers.get("X-GitHub-Event")
    data = request.json  
    
    print("Event:", event)   

    # PUSH EVENT
    if event == "push":
        change_obj = {
            "request_id": data["head_commit"]["id"],
            "author": data["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": data["head_commit"]["timestamp"]
        }
        print(change_obj)

    # PULL REQUEST EVENT
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
        print(change_obj)

    else:
        print("Event:", event)

    return "", 200


if __name__ == "__main__":
    app.run(debug=True)