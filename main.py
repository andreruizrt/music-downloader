#!/usr/bin/python

from moviepy.editor import *
from pytube import YouTube
import urllib.request

import os
import time

import re


class Config:
    DOWNLOAD_CAPACITY = 15
    link = False

            

def searchYoutube():
    search_entry = ""
    
    if Config.link == True:
        search_entry = input("Youtube ID: ")
        search_entry = [search_entry,]
        return search_entry

    else:
        search_entry = input("Search Term: ")

        try:

            search_entry = search_entry.replace(' ', '+')
            # print("You wrote: {}".format(search_entry))

            html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={search_entry}&sp=EgQQARgB")
            html = html.read().decode()

            print("[*] Getting Videos IDs...\n")
            video_ids = re.findall(r"watch\?v=(\S{11})", html)[0:Config.DOWNLOAD_CAPACITY]

            for id, value in enumerate(video_ids):
                yt = YouTube(f'https://youtube.com/watch?v={value}&sp=EgQQARgB')
                print(id, value, "\t", yt.title)
                
            return video_ids

        except:

            print("[*] Somenthing Went Wrong! Exiting...")
            exit(0)

       

def downloadVideo(video_list):

    print("[*] Downloading videos...\n")

    for video in video_list:
        try:
            print(f"[*] Downloading Video ID: {video}")
            yt = YouTube(f'https://youtube.com/watch?v={video}&sp=EgQQARgB')
            print(f"[*] Video Title: {yt.title}")
            # print("[*] Getting The Audio... {}".format(yt.streams.get_audio_only().download("./downloads/""))
            yt.streams.first().download("./downloads/")            
        except:
            print("[*] Something Went Wrong!")
        finally:
            print("[*] Success! Video Downloaded!")


def videoConvert():
    print("[*] Converting Videos...\n")
    name_video = list()
    dir_entries = os.scandir('downloads/')
    
    for entry in dir_entries:
        if entry.is_file():
            name_video.append(entry.name)

    try:    
        if not name_video:
            print("[*] The folder is empty!")
            exit(0)
        else:
            for video in name_video:
                print("[*] Tentando Arquivo:", video)

                videoclip = VideoFileClip("./downloads/{}".format(video))
                print("[*] Salvando Arquivo...")
                audioclip = videoclip.audio
                
                try:
                    audioclip.write_audiofile("./audio/{}".format(video).replace('4', '3'))
                except:
                    video = "audio_{}.mp3".format(round(time.time() * 1000))
                    print("[*] Changing video name to:", video)
                    audioclip.write_audiofile("./audio/{}".format(video))
                finally:
                    videoclip.close()
                    audioclip.close()

    except:
        print("[*] Something Went Wrong!")
        exit(0)


def deletingFolder():
    folder_name = "./downloads/"
    
    try:
        os.system("rm -rf {}".format(folder_name))
    except:
        print("[*] It was not possible delete!", folder_name)



def option_menu():
    pass



video_id = searchYoutube()
downloadVideo(video_id)
videoConvert()
deletingFolder()