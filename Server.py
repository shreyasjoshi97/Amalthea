from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hi"


@app.route("/", methods=["POST"])
def send_data():
    return "Message received!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
