from flask import Flask, request, jsonify
from music import Music
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/music")
def musicList():
    

if __name__ == '__main__':
    app.run(debug = True)