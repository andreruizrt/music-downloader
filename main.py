from moviepy.editor import *
from pytube import YouTube
import urllib.request

import os
import sys
cur_path = os.path.realpath(__file__)
base_path = os.path.dirname(os.path.dirname(cur_path))

import re

print(cur_path)
print(base_path)



class Config:
    DOWNLOAD_CAPACITY = 10
    # parallel processing - Future feature
    PARALLEL = False
    audio_downloaded_path = cur_path.replace("main.py", "mp4_audio/")
    audio_converted_path = cur_path.replace("main.py", "mp3_audio/")

def searchYoutube():
    search_entry = ""

    try:
        search_entry = input("Search: ")
        search_entry = search_entry.replace(' ', '+')
        # print("You wrote: {}".format(search_entry))

        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={search_entry}&sp=EgQQARgB")
        html = html.read().decode()
        print("[*] Getting Videos IDs...")
        video_ids = re.findall(r"watch\?v=(\S{11})", html)[0:Config.DOWNLOAD_CAPACITY]

        for id, value in enumerate(video_ids):
            yt = YouTube(f'https://youtube.com/watch?v={value}&sp=EgQQARgB')
            print(id, value, "\t", yt.title)
            
        return video_ids

    except:
        print("\nBye!")
        exit(0)

       

def search_sanitizer(search_result):
    pass



def downloadVideo(video_list):
    print("[*] Downloading videos...")
    for video in video_list:
        try:
            print(f"[*] Downloading Video ID: {video}")
            yt = YouTube(f'https://youtube.com/watch?v={video}&sp=EgQQARgB')
            print(f"Video Title: {yt.title}")
            print("[*] Getting The Audio... {}".format(yt.streams.get_audio_only().download(Config.audio_downloaded_path)))
            # yt.streams.first().download("./downloads/")            
        except:
            print("Something Went Wrong!")
        finally:
            print("[*] Exiting Video Download Function")


def videoConvert():

    pass


video_ids = searchYoutube()
downloadVideo(video_ids)
