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
    music_author = data['author']
    music_source = data['source']
    if (music_source == 'youtube'):
        music_url = data['music_url']
        music_info = music.downloadYoutubeMusic(music_url)
        return jsonify({"message": "Uploaded new music.",
            "music_title": music_info['music_title'],
            "music_path": music_info['music_path'],
            "music_author": music_author,
            }), 201
    else:
        return jsonify({"message": "Uploaded new music."}), 201

if __name__ == '__main__':
    app.run(debug = True)