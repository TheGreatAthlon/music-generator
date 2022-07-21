from midiutil import MIDIFile
import fileinput, random, os
import tkinter as tk
from tkinter import filedialog
def customDrumbeat(i, j):
    global MyMIDI, beats_per_measure, vol
    if j==0:
        MyMIDI.addNote(1,9,51, i+j, 1, vol+15)
        return
    if j%2==0 and random.randint(1,3)==1: # weakerdownbeat
        MyMIDI.addNote(1,9,36, i+j, 1, vol+15)
        MyMIDI.addNote(1,9,42, i+j, 1, vol+15)
        return
    if j%2==1 and random.randint(1,3): # weak upbeat
        MyMIDI.addNote(1,9,44, i+j, 1, vol+15)
        if random.randint(1,  3)==1:         MyMIDI.addNote(1,9,36, i+j+0.5, 1, vol+15)
        return

def word_the():
    global time, tonic, MyMIDI, track, channel,  volume, duration_mod, volume_mod
    MyMIDI.addNote(track, channel, tonic+10, time, 0.25*duration_mod, volume+volume_mod)
    MyMIDI.addNote(track, channel, tonic+12, time, 0.25*duration_mod, volume+volume_mod)
    MyMIDI.addNote(track, channel, tonic+16, time, 0.25*duration_mod, volume+volume_mod)
    time+=0.25

def word_and():
    global time, tonic, MyMIDI, track, channel, volume, duration_mod, volume_mod
    MyMIDI.addNote(track, channel, tonic-5, time, 0.25*duration_mod, volume+volume_mod)
    MyMIDI.addNote(track, channel, tonic+5, time, 0.25*duration_mod, volume+volume_mod)
    MyMIDI.addNote(track, channel, tonic+11, time, 0.25*duration_mod, volume+volume_mod)
    time+=0.25

def char_group_sh():
    global time, tonic, MyMIDI, track, channel, volume, duration_mod, volume_mod
    MyMIDI.addNote(track, channel, tonic+12, time, 0.25*duration_mod, volume+volume_mod)
    MyMIDI.addNote(track, channel, tonic+16, time, 0.25*duration_mod, volume+volume_mod)
    time+=0.333
def char_group_ei():
    #print("char group ei detected")
    global time, tonic, MyMIDI, track, channel, volume, duration_mod, volume_mod
    MyMIDI.addNote(track, channel, tonic-5, time, 0.25*duration_mod, volume+volume_mod-20)
    MyMIDI.addNote(track, channel, tonic, time, 0.25*duration_mod, volume+volume_mod-20)
    time+=0.25
def char_group_it():
    global time, tonic, MyMIDI, track, channel, volume, duration_mod, volume_mod
    MyMIDI.addNote(track, channel, tonic+7, time, 0.5*duration_mod, volume+volume_mod-20)
    MyMIDI.addNote(track, channel, tonic+10, time, 0.5*duration_mod, volume+volume_mod-20)
    time+=0.25

def char_group_tion():
    global time, tonic, MyMIDI, track, channel, volume, duration_mod, volume_mod
    MyMIDI.addNote(track, channel, tonic-13, time, 0.25*duration_mod, volume+volume_mod-20)
    MyMIDI.addNote(track, channel, tonic-5, time+0.25, 0.25*duration_mod, volume+volume_mod-20)
    MyMIDI.addNote(track, channel, tonic+2, time+0.5, 0.25*duration_mod, volume+volume_mod-20)
    MyMIDI.addNote(track, channel, tonic+5, time+0.75, 0.25*duration_mod, volume+volume_mod-20)
    time+=0.5

def word_it():
    global time, tonic, MyMIDI, track, channel, volume, duration_mod, volume_mod
    MyMIDI.addNote(track, channel, tonic+7, time, duration_mod, volume+volume_mod)
    MyMIDI.addNote(track, channel, tonic+10, time, duration_mod, volume+volume_mod)
    MyMIDI.addNote(track, channel, tonic+12, time, duration_mod, volume+volume_mod)
    time+=0.25
nodrum=[]
root = tk.Tk()      
root.withdraw()
charGroupStats={}
wordStats={}
file_path = filedialog.askopenfilename()
#print("OK, working with "+file_path)
lines=[]
with fileinput.input(files=file_path) as f:
	for line in f:
		lines.append(line[0:len(line)])

maintonic=60
tonic=maintonic #middle c
# pitch values are expressed as semitones from the tonic.

char_assoc={"s": 12, "r": 7, "a": -7, "e": 0, "i": -5, "o": -12, "u": -3, "t": 10, "h": 16, "w": 9, "l": 5, "g": -8, "n":-3,"c": 21, "d": 4, "p": -17, "k": 24, "m": 17, "b": -14}

track    = 0
channel  = 0
duration = 0.5   # In beats
tempo=random.randint(112,143)  # In BPM
volume   = 76 # 0-127, as per the MIDI standard
volume_mod=0
beats_per_measure=random.randint(3,7)
time     = beats_per_measure+1   # In beats
MyMIDI = MIDIFile(2) # 2 tracks
MyMIDI.addTempo(track,0, tempo)
skip=0
word_tonic_mod=0
duration_mod=1 #duration mod for stacatto notes
for line in lines:
    for w in line.split(" "):
        time=round(time+0.5)
#print(w)
        if len(w)>0 and w[len(w)-1]=="!":
            #print("! end of word detected")
#            word_tonic_mod=9
            tonic+=9
            duration_mod=0.06
            volume_mod=35
        if ("word_"+w.lower()) in globals():
            globals()["word_"+w.lower()]();
            if not (w.lower() in wordStats): wordStats[w.lower()]=0
            wordStats[w.lower()]+=1
        else:
            duration=0.25*int(len(w))
            if len(w)>0 and w[0].isalpha(): startChar=w[0].lower()
            else: startChar="b"
            wordIndex=0
            firsstvol=0
            for c in w:
                if time%beats_per_measure==0: firstvol=1
                else: firstvol=0
                if skip>0:
                    skip-=1
                    wordIndex+=1
                    continue
                if c==".":
                    MyMIDI.addNote(1, 9, 38, time, 1, 100)
                    MyMIDI.addNote(1, 9, 36, time+0.25, 1, 100)
                    MyMIDI.addNote(1, 9, 35, time+0.5, 1, 100)
                    nodrum.append((time,time+2))
                    time+=1
                if c==":":
                    wheelspin=time-1
                    bend=0
                    semitonebend=0
                    while wheelspin<=time:
                        MyMIDI.addPitchWheelEvent(track,channel,wheelspin,bend)
                        wheelspin+=1/100
                        bend+=80
                    time+=0.5*duration
                    MyMIDI.addPitchWheelEvent(track,channel,time,0)
                    wordIndex+=1
                    continue
                bigram="";
                bigramMatch=0
                for l in range(6,1,-1):
                    if wordIndex<len(w)-l-1: bigram=w[wordIndex:wordIndex+l].lower()
                    if ("char_group_"+bigram) in globals():
                        globals()["char_group_"+bigram]()
                        bigramMatch=1
                        if not (bigram in charGroupStats): charGroupStats[bigram]=0
                        charGroupStats[bigram]+=1
                        wordIndex+=l
                        skip=l
                        break
                if bigramMatch==1: continue;
                if c.isupper() and c.lower() in char_assoc:
                    tonic=maintonic+char_assoc[c.lower()]
                if c.lower() in char_assoc:
                    #print(w+" duration will be "+str(duration*duration_mod)+", was originally "+str(duration))
                    MyMIDI.addNote(track, channel, tonic+char_assoc[c.lower()], time+(random.randint(4+len(w),14+len(w))/100), duration*duration_mod, volume+volume_mod)
                    if startChar=="a" or startChar=="e" or startChar=="i" or startChar=="o" or startChar=="u" or len(w)>5:
                        time+=duration/max(2,len(w)-2)
                wordIndex+=1
            time+=min(2,duration/4)
        duration_mod=1
        volume_mod=0
    tonic=maintonic

total_time=int(time)
#drum track
MyMIDI.addProgramChange(1, 9, 0, 8)
for i in range(1,beats_per_measure+1):
    MyMIDI.addNote(1,9,31,i,0.25,100)
MyMIDI.addTimeSignature(0,0,beats_per_measure,2, 24)
downbeat=[38, 40, 65, 66]
vol=70
for i in range(beats_per_measure+1,total_time+1,beats_per_measure):
    subdivisions=random.randint(0,4)
    subdivisions=max(subdivisions,2)
    #print("beat "+str(i))
    nodrums=0
    for ndr in nodrum:
        if i+beats_per_measure>=ndr[0] and i+beats_per_measure<ndr[1]: nodrums=1
    if nodrums==1: continue
    for j in range(0, beats_per_measure):
        custom=random.randint(1,6)
        if custom>=4:
            customDrumbeat(i,j)
            continue
        for k in range(0, subdivisions):
            drum=random.choice(downbeat)
            voll=45
            if j==0 and k==0:
                drum=55
                vol=90
            else: vol=70
            if random.randint(1,5)>=2: MyMIDI.addNote(1,9, drum, i+j+k*round(1/subdivisions,3), round(1/subdivisions,3), vol-4)

MyMIDI.addTrackName(1,0,"drums")
with open(os.path.basename(file_path)+"_music.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
    print("Finished. word stats: "+str(wordStats)+", Char group stats:" +str(charGroupStats))