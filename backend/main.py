from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import library.music as Music

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Welcome to sommie radio ! Let's share music."

@app.route("/music")
def musicList():
    musicList = Music.load_music_list()
    return jsonify(musicList)

@app.route("/playlist")
def playList():
    play_list = Music.load_playlist()
    return jsonify(play_list)

@app.route("/streaming")
def streaming():
    def generate():
        play_list = Music.load_playlist()
        music_id = play_list[0]['id']
        music_file = Music.load_music(music_id)['music_path']
        
        with open(music_file, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)

                    
    return Response(generate(), mimetype="audio/mp3")
                

#Able user to upload their own music file, or loading music from video website
@app.route('/music', methods = ['POST'])
def uploadMusic():
    data = request.get_json()
    music_author = data['author']
    music_source = data['source']
    if (music_source == 'youtube'):
        music_title = data['music_title']
        music_url = data['music_url']
        music_info = Music.download_youtube_music(music_title, music_url)
        music_info['music_title'] = music_title
        music_info['music_author'] = music_author
        music_info['music_source'] = music_source
        
        # Save the music information
        Music.save_music(music_info)
        
        return jsonify({"message": "Uploaded new music.",
            "music_title": music_info['music_title'],
            "music_path": music_info['music_path'],
            "music_author": music_author,
            }), 201
        
    if (music_source == 'bilibili'):
        data = request.get_json()
        music_title = data['music_title']
        music_url = data['music_url']
        music_author = data['author']
        music_source = data['source']
        music_info = Music.download_bili_video(music_title, music_url)
        
        music_info['music_title'] = music_title
        music_info['music_author'] = music_author
        music_info['music_source'] = music_source
        
        Music.save_music(music_info)
        
        return jsonify({"message": "Uploaded new music.",
                        "music_title": music_info['music_title'],
                        "music_path": music_info['music_path'],
                        "music_author": music_author,
                        }), 201
    else:
        return jsonify({"message": "Uploaded new music."}), 201

if __name__ == '__main__':
    app.run(debug = True)