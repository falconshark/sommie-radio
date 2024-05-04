from flask import Flask, request, jsonify
import music

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/music")
def musicList():
    musicList = music.load_music_list()
    return jsonify(musicList)

#Able user to upload their own music file, or loading music from video website
@app.route('/music', methods = ['POST'])
def uploadMusic():
    data = request.get_json()
    music_author = data['author']
    music_source = data['source']
    if (music_source == 'youtube'):
        music_url = data['music_url']
        music_info = music.download_youtube_music(music_url)
        return jsonify({"message": "Uploaded new music.",
            "music_title": music_info['music_title'],
            "music_path": music_info['music_path'],
            "music_author": music_author,
            }), 201
    if (music_source == 'bilibili'):
            data = request.get_json()
            music_url = data['music_url']
            music_author = data['author']
            music_source = data['source']
            music_info = music.download_bili_video(music_url)
            return jsonify({"message": "Uploaded new music.",
                            "music_title": music_info['music_title'],
                            "music_path": music_info['music_path'],
                            "music_author": music_author,
                            }), 201
    else:
        return jsonify({"message": "Uploaded new music."}), 201

if __name__ == '__main__':
    app.run(debug = True)