dimensions = 330,525






from pathlib import Path
from pydub import AudioSegment as AS
from pydub.playback import play
from tkinter import filedialog
from datetime import datetime
import tkinter as tk
import pyautogui as pyag
import shutil
import threading
import time
import os
os.chdir(Path(__file__).parent)
window = tk.Tk()
window.title("poopify")
window.geometry(f"{str(dimensions[0])}x{str(dimensions[1])}")
label = tk.Label(window,text = "              poopify",font = ("Arial",20))
label.grid(column = 0,row = 0)


def addSong():
    fp = filedialog.askopenfilenames()
    for path in fp:
        exts = path.split(".")
        ext = exts[len(exts)-1]
        if(ext != "mp3"):
            alert("The programmer was too lazy to add in support for other file formats, so deal with it")
            return
    for src in fp:
        filename = src.split("/")[len(src.split("/"))-1]
        shutil.copyfile(src,f"songs/{filename}")
add = tk.Button(window,text = "add song",bg = "black",fg = "white",command = addSong,font = ("Arial",20))
add.grid(column=0,row = 1)

def createPlaylist():
    fp = filedialog.askopenfilenames()
    if(fp == ""):
        return
    for path in fp:
        exts = path.split(".")
        ext = exts[len(exts)-1]
        if(ext != "mp3"):
            alert("The programmer was too lazy to add in support for other file formats, so deal with it")
            return
    name = pyag.prompt("playlist name")
    if(name == "" or name == None):
        alert("please fill in a valid playlist name")
        return
    os.makedirs(f"playlists/{name}")
    for src in fp:
        filename = src.split("/")[len(src.split("/"))-1]
        shutil.copyfile(src,f"playlists/{name}/{filename}")
    alert("playlist successfully created")
create = tk.Button(window,text = "create playlist",bg = "gray",fg = "white",command = createPlaylist,font = ("Arial",20))
create.grid(column = 0,row = 2)

def addTo():
    playlist = pyag.prompt("which playlist do you want to add to")
    if(os.path.isdir(f"playlists/{playlist}") == False):
        alert("playlist not found")
        return
    fp = filedialog.askopenfilenames()
    for path in fp:
        exts = path.split(".")
        ext = exts[len(exts)-1]
        if(ext != "mp3"):
            alert("The programmer was too lazy to add in support for other file formats, so deal with it")
            return
    for src in fp:
        filename = src.split("/")[len(src.split("/"))-1]
        shutil.copyfile(src,f"playlists/{playlist}/{filename}")
    alert("songs successfully added")
add = tk.Button(window,text = "add to playlist",bg = "pink",fg = "black",command = addTo,font = ("Arial",20))
add.grid(column = 0,row = 3)

def alert(msg):
    def main():
        pyag.alert(msg)
    threading.Thread(target=main).start()

class main():
    def __init__(self):
        self.start = tk.Button(window,text = "select",bg = "white",fg = "purple",command = self.select,font = ("Arial",20))
        self.start.grid(column = 0,row = 4)
        self.PAUSE = tk.Button(window,text = "pause",bg = "white",fg = "red",command = self.Pause,font = ("Arial",20))
        self.PAUSE.grid(column = 0,row = 6)
        self.PLAY = tk.Button(window,text = "play",bg = "white",fg = "green",command = self.Play,font = ("Arial",20))
        self.PLAY.grid(column = 0,row = 5)
        self.SKIP = tk.Button(window,text = "skip",bg = "orange",fg = "white",command = self.Skip,font = ("Arial",20))
        self.SKIP.grid(column = 0,row = 7)

        self.selected = []
        self.current = [0,0]
        self.start_time = 0
        self.paused = False
        self.cur_song = None
        self.t = None
        self.kill = False
    def select(self):
        ans = 0
        while(True):
            choice = pyag.prompt("1: select playlist\n2: select songs individually")
            if(choice == "1" or choice == "2"):
                ans = int(choice)
                break
            elif(choice == None):
                return
            else:
                alert("invalid input")
        if(ans == 1):
            fp = filedialog.askdirectory()
            if(str(Path(fp).parent) == os.path.join(os.getcwd(),"playlists")):
                selected = []
                for dirs, subdirs, files in os.walk(fp):
                    for file in files:
                        if(file.split(".")[len(file.split("."))-1] == "mp3"):
                            self.selected.append(os.path.join(fp,file))
            else:
                alert("invalid location")
                return
        elif(ans == 2):
            fps = filedialog.askopenfilenames()
            if(fps == ""):
                return
            self.selected = []
            for file in fps:
                if(file.split(".")[len(file.split("."))-1] == "mp3"):
                    self.selected.append(file)
        else:
            alert("how did u get here?")
            return
        current = [0,0]
    def Pause(self):
        go = False
        try:
            if(self.cur_song.playback.is_playing() == True):
                go = True
        except:
            pass
        if(go == True):
            self.paused = True
            self.cur_song.playback.stop()
            self.current[1] = round(round(datetime.now().timestamp(),3)*1000) - self.start_time
        else:
            alert("no song is playing yet, moron")
            return
    def Play(self,skip = 0):
        def main(skip):
            go = False
            try:
                if(self.cur_song == None):
                    go = True
                elif(self.cur_song.playback.is_playing() == False):
                    go = True
            except:
                pass
            if(go == True):
                if(self.selected == []):
                    alert("No songs selected")
                    return
                for i,songname in enumerate(self.selected[self.current[0] + skip:]):
                    self.paused = False
                    self.current[0] = i
                    try:
                        song = AS.from_mp3(songname)[self.current[1]:]
                    except:
                        alert("song could not be opened")
                        return
                    self.cur_song = play(song)
                    self.start_time = round(round(datetime.now().timestamp(),3)*1000)
                    while(self.paused == False):
                        if(self.kill == True):
                            self.kill = False
                            return
                    
            else:
                alert("song is alreay playing, moron")
                return
        if(self.t != None):
            self.kill = True
            while(self.kill):
                pass
        self.t = threading.Thread(target=main,args=(skip,)).start()
    def Skip(self):
        self.Pause()
        self.Play(skip = 1)
m = main()
