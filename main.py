from flask import Flask, request, jsonify
import music

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/music")
def musicList():
    musicList = music.loadMusicList()
    return jsonify(musicList)

#Able user to upload their own music file, or loading music from video website
@app.route('/music', methods = ['POST'])
def uploadMusic():
    data = request.get_json()
    music_type = data['type']
    if (music_type == 'online'):
        

    return jsonify({"message": "Uploaded new message."}), 201

if __name__ == '__main__':
    app.run(debug = True)