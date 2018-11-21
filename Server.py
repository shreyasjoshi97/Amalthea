from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def index():
    return "Hi"


@app.route("/", methods=["POST"])
def send_data():
    return "Message received!"


if __name__ == "__main__":
    port = int(os.environ.get('Port', 5000))
    app.run(host='0.0.0.0', port=port)
