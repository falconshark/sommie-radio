import sqlite3
import os
from pydub import AudioSegment
from pytube import YouTube

class Music:
   def __init__(self, id, title, author):
      self.id = id
      self.title = title
      self.author = author

def loadMusicList():
    conn = sqlite3.connect('sommie.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM music')
    print(cur.fetchall())
    cur.close()
    conn.close()

# Download Youtube video and convert it to mp3 file.
def downloadYoutubeMusic(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    destino = "saved_music"
    out_file = video.download(output_path=destino)
    base, ext = os.path.splitext(out_file)

    audio = AudioSegment.from_file(out_file)
    new_file = base + '.mp3'
    audio.export(new_file, format='mp3')
    #Remove old video file.
    os.remove(out_file)

    #return music info to main process.
    music_info = {
        "music_title": yt.title,
        "music_path" : destino + base + '.mp3',
    }

    return music_info