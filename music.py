import sqlite3
import os
from pydub import AudioSegment
from pytube import YouTube
import requests
import re
import json
from pathlib import Path

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

# Download Bilibili video and convert it to mp3 file.
def downloadBiliVideo(url):
    session = requests.session()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',"Referer": "https://www.bilibili.com",}
        #Able user to use their own user agent.
    resp = session.get(url,headers = headers)
    video_title = re.findall(r'<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili',resp.text)[0]
    video_info = re.findall(r'<script>window.__playinfo__=(.*?)</script>',resp.text)[0]
    json_data = json.loads(video_info)
    audio_url = json_data['data']['dash']['audio'][0]['base_url']
    audio_content = session.get(audio_url,headers=headers).content
    
    destino = "saved_music"
    Path(destino).mkdir(parents = True, exist_ok = True)
    with open(destino + '/' + video_title + '.mp3','wb') as f:
        f.write(audio_content)
    final_file_path = destino + '/' + video_title + '.mp3'
    return {
        "music_title": video_title,
        "music_path" : final_file_path,
        }