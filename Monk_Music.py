import threading
from tkinter import *
import time
from pygame import mixer
import os
from mutagen.mp3 import MP3
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import themed_tk
from tkinter import ttk

root = themed_tk.ThemedTk()
root.get_themes()
root.set_theme('arc')
root.title("Monk_Music")
root.minsize(490, 250)
root.maxsize(490, 250)
root.iconbitmap(r'newwlogoo.ico')

status_bar = ttk.Label(root, text="Gaana Sun Lo FRIENDS", relief=SUNKEN, anchor=W, font="Times 10 bold")
status_bar.pack(side=BOTTOM, fill=X)

left_frame = Frame(root)
left_frame.pack(side=LEFT, padx=15)

welcome = ttk.Label(root, text="Welcome to MONK MUSIC", font="Times 10 bold")
welcome.pack(side=TOP)

right_frame = Frame(root)
right_frame.pack(side=TOP, pady=10)

f1 = Frame(right_frame)
f1.pack()

f2 = Frame(right_frame)
f2.pack(pady=20)

FileName = "Gaana sun lo Fraands"

music_list = []


def browse_files():
    global FileName
    FileName = filedialog.askopenfilename(title="Select Music", filetypes=(("mp3 Files", "*.mp3"),))
    add_files_playlist(FileName)


def add_files_playlist(f):
    f = os.path.basename(str(FileName))
    index_ = 0
    play_list.insert(index_, f)
    music_list.insert(index_, FileName)
    index_ += 1


def show_info(i):
    audio = MP3(music_list[i])
    total_l = audio.info.length
    min_s, secs = divmod(total_l, 60)
    min_s = round(min_s)
    secs = round(secs)
    F_length['text'] = f'Length 0{min_s} : {secs}'


meBar = Menu(root)
root.config(menu=meBar)

sm1 = Menu(meBar)
meBar.add_cascade(label="File", menu=sm1)
sm1.add_command(label="Open", command=browse_files)
sm1.add_command(label="Exit", command=root.destroy)

mixer.init()


def showC_time(i):
    audio = MP3(music_list[i])
    t = int(audio.info.length)
    while t > 0 and mixer.music.get_busy():
        min_s, secs = divmod(t, 60)
        min_s = round(min_s)
        secs = round(secs)
        C_length['text'] = f'Length 0{min_s} : {secs}'
        time.sleep(1)
        t -= 1


def playM():
    global paused
    if paused:
        mixer.music.unpause()
        status_bar['text'] = os.path.basename(str(FileName))
        paused = FALSE
    if FileName != 'Gaana sun lo Fraands' and play_list.curselection():
        stop()
        time.sleep(1)
        slected_F = play_list.curselection()
        slected_index = slected_F[0]
        mixer.music.load(music_list[slected_index])
        mixer.music.play()
        status_bar['text'] = os.path.basename(music_list[slected_index])
        mixer.music.set_volume(0.4)
        show_info(slected_index)
        t1 = threading.Thread(target=showC_time, args=(slected_index,))
        t1.start()
    elif FileName == 'Gaana sun lo Fraands':
        messagebox.showerror(title="No file selected", message="File select kar Lawde🤣😂😂")


def set_vol(vol_v):
    v = float(vol_v) / 200
    mixer.music.set_volume(v)
    if v > 0:
        muteB.configure(image=un_muteP)


paused = FALSE


def pauseM():
    global paused
    paused = TRUE
    mixer.music.stop()
    status_bar['text'] = 'Paused'


muted = FALSE


def mute():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        muteB.configure(image=un_muteP)
        volumeBar.set(100)
        muted = FALSE
    else:
        muted = TRUE
        mixer.music.set_volume(0)
        muteB.configure(image=muteP)
        volumeBar.set(0)


def stop():
    mixer.music.stop()


playP = PhotoImage(file="play-button.png")
playB = ttk.Button(f1, image=playP, command=playM,)
playB.pack(side=LEFT)

pauseP = PhotoImage(file="pause (1).png")
pauseB = ttk.Button(f1, image=pauseP, command=pauseM)
pauseB.pack(side=LEFT)

stopP = PhotoImage(file="stop-button.png")
stopB = ttk.Button(f1, image=stopP, command=stop)
stopB.pack(side=LEFT)

muteP = PhotoImage(file="emoji.png")
un_muteP = PhotoImage(file="emoji (1).png")
muteB = ttk.Button(f2, image=un_muteP, command=mute)
muteB.grid(row=0, column=0)

volumeBar = ttk.Scale(f2, from_=0, to=200, orient=HORIZONTAL, command=set_vol)
volumeBar.grid(row=0, column=1)
volumeBar.set(80)

F_length = ttk.Label(f2, text="Total Length --:--", font="Times 10")
F_length.grid(row=1, column=0)

C_length = ttk.Label(f2, text="Current Length --:--", font="Times 10")
C_length.grid(row=1, column=1)


def on_closing():
    if messagebox.askyesno(title='Closing Window',
                           message='Saach Me Baand Karna Chahate Hai Bhai.\nMat kar bol raha hoon'):
        stop()
        root.destroy()
    else:
        pass


root.protocol("WM_DELETE_WINDOW", on_closing)


# left frame content

def del_file():
    if not music_list:
        messagebox.showerror(title='No item in playlist', message="Playlist Empty hai Bhai")
    elif play_list.curselection():
        slected_F = play_list.curselection()
        slected_index = slected_F[0]
        play_list.delete(slected_index)
        music_list.pop(slected_index)


play_L = ttk.Label(left_frame, text="PLAYLIST", font="Times 10 bold")
play_L.pack(side=TOP)

play_list = Listbox(left_frame)
play_list.pack()

add_M = ttk.Button(left_frame, text='+ Add', command=browse_files)
add_M.pack(side=LEFT)

del_M = ttk.Button(left_frame, text='- Remove', command=del_file)
del_M.pack(side=LEFT)

root.mainloop()
