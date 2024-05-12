import sqlite3
import os
from pydub import AudioSegment
from pytube import YouTube
import requests
import re
import json
from pathlib import Path

def load_music_list():
    music_list = []
    conn = sqlite3.connect('./sommie.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM music')
    sql_result = cur.fetchall()
    cur.close()
    conn.close()
    
    for result in sql_result:
        music = {
            'id': result[0],
            'title': result[1],
            'author': result[2],
            'file_path': result[3],
        }
        music_list.append(music)
        
    return music_list

def load_playlist():
    playlist = []
    conn = sqlite3.connect('./sommie.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM playlist')
    sql_result = cur.fetchall()
    cur.close()
    conn.close()
    
    for result in sql_result:
        music = {
            'order': result[0],
            'id': result[1],
        }
        playlist.append(music)
    
    return playlist

def load_music(id):
    conn = sqlite3.connect('./sommie.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM music where id=?;", (id,))
    sql_result = cur.fetchone()
    
    music = {
        'id': sql_result[0],
        'author': sql_result[2],
        'music_path': sql_result[3],
        'title': sql_result[1]
    }
    
    cur.close()
    conn.close()
    return music
    
def save_music(music_info):
    conn = sqlite3.connect('./sommie.db')
    cur = conn.cursor()
    music_title = music_info['music_title']
    music_path = music_info['music_path']
    music_author = music_info['music_author']
    
    #Insert new music to the database.
    cur.execute("INSERT INTO music(title, file_path, author) values(?, ?, ?);", (music_title, music_path, music_author))
    conn.commit()
    cur.close()
    conn.close()
    
    # Download Youtube video and convert it to mp3 file.
def download_youtube_music(music_title, url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    destino = "saved_music/"
    out_file = video.download(output_path = destino)
    
    audio = AudioSegment.from_file(out_file)
    new_file = destino + music_title + '.mp3'
    audio.export(new_file, format='mp3')
    #Remove old video file.
    os.remove(out_file)

    #return music info to main process.
    music_info = {
        "video_title": yt.title,
        "music_path" : destino + music_title + '.mp3',
        }
    return music_info
    
    # Download Bilibili video and convert it to mp3 file.
def download_bili_video(music_title, url):
    session = requests.session()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',"Referer": "https://www.bilibili.com",}
    # Able user to use their own user agent.
    
    resp = session.get(url,headers = headers)
    video_title = re.findall(r'<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili',resp.text)[0]
    video_info = re.findall(r'<script>window.__playinfo__=(.*?)</script>',resp.text)[0]
    json_data = json.loads(video_info)
    audio_url = json_data['data']['dash']['audio'][0]['base_url']
    audio_content = session.get(audio_url,headers=headers).content
    
    destino = "saved_music"
    Path(destino).mkdir(parents = True, exist_ok = True)
    with open(destino + '/' + music_title + '.mp3','wb') as f:
        f.write(audio_content)
        final_file_path = destino + '/' + music_title + '.mp3'
        return {
            "video_title": video_title,
            "music_path" : final_file_path,
        }