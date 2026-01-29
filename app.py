from flask import Flask, request, json

app = Flask(__name__)

@app.route("/")
def health():
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    print("Received webhook!")
    print(request.json)
    return "", 200


if __name__ == "__main__":
    app.run(debug=True)