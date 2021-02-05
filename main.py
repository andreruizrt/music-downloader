#!/usr/bin/env

import time
from moviepy.editor import *
from pytube import YouTube
import urllib.request

import os
import sys
cur_path = os.path.realpath(__file__)

import re


class Config:
    DOWNLOAD_CAPACITY = 10
    # parallel processing - Future feature
    PARALLEL = False
    downloaded_path = cur_path.replace("main.py", "mp4_audio/")
    converted_path = cur_path.replace("main.py", "mp3_audio/")

def searchYoutube():
    search_entry = ""

    try:
        search_entry = input("Search Term: ")
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
        print("[*] Somenthing Went Wrong...")
        print("[*] Exiting Program...")
        exit(0)

       

def search_sanitizer(search_result):
    pass



def downloadVideo(video_list):
    print("[*] Downloading videos...")
    for video in video_list:
        try:
            print(f"[*] Downloading Video ID: {video}")
            yt = YouTube(f'https://youtube.com/watch?v={video}&sp=EgQQARgB')
            print(f"[*] Video Title: {yt.title}")
            # print("[*] Getting The Audio... {}".format(yt.streams.get_audio_only().download(Config.downloaded_path)))
            yt.streams.first().download("./downloads/")            
        except:
            print("[*] Something Went Wrong!")
        finally:
            print("[*] Exiting Video Download Function")


def videoConvert():
    name_video = list()
    dir_entries = os.scandir('downloads/')
    
    for entry in dir_entries:
        if entry.is_file():
            name_video.append(entry.name)

    try:    
        if not name_video:
            print("[*] A pasta esta vazia!")
            exit(0)
        else:
            for video in name_video:
                # mp4_file = './downloads/' + video
                # print(mp4_file)
                # mp3_file = './downloads/' + video
                # mp3_file = str(mp3_file).replace('4', '3')
                # print(mp3_file)

                print("[*] Tentando Arquivo:", video)

                videoclip = VideoFileClip("./downloads/{}".format(video))
                print("[*] Salvando Arquivo...")

                audioclip = videoclip.audio
                audioclip.write_audiofile("./audio/{}".format(video).replace('4', '3'))

                videoclip.close()
                audioclip.close()

    except:
        print("[*] Something Went Wrong!")


# video_ids = searchYoutube()
# downloadVideo(video_ids)
videoConvert()