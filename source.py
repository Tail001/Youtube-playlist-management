import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import re
#progress bar
from time import sleep
from tqdm import tqdm, trange
import tkinter as tk

#information
channel_id = 'UCJL0OWDUQaXmWSZ_u4-woPw'
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

title = [] # It seems useless in this project

def print_text(x):
    if x == 1:
        print('Input the keyword to execute: \n')
        print('Add video to playlist : 1')
        print('Delete video from playlist: 2')
        print('Search the video: 3')
        print('delete or add a new playlist : 4')
        print('Change position in a playlist: 5')
        print('Leave: x\n')


def add_to_playlist(playlist_id):
    
    url = re_to_find_id()
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            'snippet': {
              'playlistId': playlist_id, 
              'resourceId': {
                      'kind': 'youtube#video',
                  'videoId': url
                }
            #'position': 0
            }
        }
    )
    response = request.execute()
    #print(response)
    
def delete_playlistItem(playlist_id):
    
    video_id = re_to_find_id()
    
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        videoId= video_id
    )
    response = request.execute()    
    #print(response['items'])
    #print(type(response))
    real_id = response['items'][0]['id']
    #print(real_id)
    request = youtube.playlistItems().delete(
        id=real_id
    )
    request.execute()

def change_position(playlist_id):
    video_id = re_to_find_id() 
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        videoId= video_id
    )
    response = request.execute()
    next_id = response['items'][0]['id']
    #print(next_id)
    #print(response)
    position = int(input('Input the position (start from 0): '))
    request = youtube.playlistItems().update(
        part="id, snippet",
                    body={
                        "id":next_id ,
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            },
                            "position": position
                        }
                    }
                ).execute()  
    for i in trange(100):
        sleep(0.001)
    print('completed')
    sleep(1)

    
def list_video_in_playlist(playlist_id):
    videos = []
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlist_id
        
    )
    response = request.execute()
    num = len(response['items'])
    for i in range(num):
        objects = response['items'][i]['snippet']['title']
        print(objects)
        videos.append(objects)
    return videos
            
def re_to_find_id():
    while True:
        try:
            regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
            url = input('Input the web address: ')
            match = regex.match(url)
            return match.group('id')
        except AttributeError :
            print('no match')
    #print(match.group('id'))  

def willness_show_playlist(x):
    display = True
    print("\nYou have %d videos in your playlist " %x)
    while(True):
        willness = input('Do you want to show the playlisy first?\n[Y]:yes [N]:no\n')
        if willness == 'Y' or willness == 'y':
            return display
        elif willness == 'N' or willness == 'n':
            display = False
            return display
        else:
            print('Plz input again')
            sleep(1)
          
def search_video(a)->str:
    while True:   
        count = 0
        key = input("Type the keywords: ")
        if key.isalpha():
        # ignore upper or lower
            r = re.compile('.*%s' %key,re.I)
        else:
            r = re.compile('.*%s' %key)        
        for i in trange(100):
            sleep(0.00001)
        print("\n\n===============================")
        for i in range(len(a)):
            match = r.search(a[i])
            
            if match:
                count += 1
                global title 
                title.append(a[i])
                print(a[i])
                
        if count == 0:
            print("Not found in the playlist\n")        
        print("===============================")
        
        leave = input('\nIf u want to leave , type X to exit\nor press any key to continue\n' )
        if leave == 'x' or leave == 'X':
            break
                      
def display_playlist(display, playlist):
    if display == True:
        sleep(1)
        for i in trange(100):
            sleep(0.0087)
        print('===============================')
        for i in playlist:
            print(i)
        print('===============================')
        

def list_video_in_playlist(playlist_id)->list:
    videos = []
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlist_id
    )
    response = request.execute()
    num = len(response['items'])
    for i in range(num):
        objects = response['items'][i]['snippet']['title']
        videos.append(objects)
        #print(videos)   
    return videos #list
def create_new_playlist():
    
    name = input('Type the name of the new playlist: ')
    request = youtube.playlists().insert(
        part="snippet",
        body={
          "snippet": {
            "title": name,
            "channelId": channel_id
          }
        }
    )
    response = request.execute()
 
def print_playlist_info()->dict:
    playlist_info = {}
    request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id
    )
    response = request.execute()

    num = len(response['items'])
    for i in range(num):
        key = response['items'][i]['snippet']['title']
        value = response['items'][i]['id']
        playlist_info[key] = value 
        
    return playlist_info #dictionary


def delete_playlist(playlist_id):
    request = youtube.playlists().delete(
        id=playlist_id
    )
    request.execute()
    print('hello, anybody here?')
    for i in trange(100):
            sleep(0.001)
    print('completed.')

def change_playlist_id(playlist_id = print_playlist_info())->str:
    print("\nNow you have %d playlists in total"%len(playlist_id))
    print("choose one to continue")
    print('===============================')
    for i, j in playlist_id.items():
        print("playlist name : %s , id: %s" %(i ,j))
    print('===============================')
    playlist_id = input('ctrl C --> ctrl V to paste id: ')
    return playlist_id
# It may not use in this project
'''
def get_video_id():
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlist_id
        
    )
    response = request.execute()
    item_number = len(response['items'])   
    if item_number == 0 :
        print('Playlist is empty.')    
        sleep(1)
    else: 
        for i in range(item_number):
            global title
            for j in range(len(title)):
                if title[j] == response['items'][i]['snippet']['title'] :  
                    video_id = response['items'][i]['id']      
                    print("Video: %s \n ID: %s" %(title[j],video_id))  
                    
'''

    
#main        
while(True):
    playlist_id = change_playlist_id()
    print_text(1)
    # choose what to do
    option = input()
    # add to the playlist
    if option == '1':
        add_to_playlist(playlist_id)
        print('\nAdding to the playlist...')
        for i in trange(100):
            sleep(0.001)
        print('completed\n')
        sleep(1)
    # delete video from playlist     
    elif option == '2':
        delete_playlistItem(playlist_id)
        print('Deleting from playlist...')
        for i in trange(100):
            sleep(0.001)
        print('completed\n')
        sleep(1)
    # search & display    
    elif option == '3':
        playlist = list_video_in_playlist(playlist_id)
        display = willness_show_playlist(len(playlist))
        display_playlist(display, playlist)
        search_video(playlist)
        #get_video_id()
        print('completed\n')
        sleep(1)
    
    # add or delete playlist
    elif option == '4':
        while True:
            query = input('Add [1] or delete [2] a playlist and [x] to exit:  ')
            if query == '1':
                create_new_playlist()
                for i in trange(100):
                    sleep(0.001)
                print('conpleted')
            elif query == '2':
                delete_playlist(playlist_id)
            
            elif query == 'x' or query =='X':
                break
            else:
                print("Error, plz input again")
    
    elif option == '5':  
        change_position(playlist_id)
        
        
    elif option == 'x' or option == 'X':
        print('Thank u and welcome next time.')
        break
       
    else:
        print('Error. plz input again')
        sleep(1)
        print()


    

#user id: UCJL0OWDUQaXmWSZ_u4-woPw   
#playlilst id : PLPtxS4ujih3X1SLQx_nIDpXf_eWpoXPaI
#reference:https://ithelp.ithome.com.tw/articles/10269436
#reference :#101 使用 YouTube Data API 抓取有趣的 Youtuber 影片 & MV