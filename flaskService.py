#! /usr/bin/python3
import glob
import os
import os.path
from os import path
import sys 




# we have to build the path to the session files
userName = "YourUserName"
histPath = "/mnt/c/Users/" + userName + "/Music/_Serato_/History/Sessions/*.session"

# Where we store the music, in windows path terms and WSL mount terms
songPathW = "C:\seraP4th"
songPathL = "/mnt/c/seraP4th/"


def getHistFile(): # return the newest "*.session" file 
    histFiles = glob.glob(histPath)
    histFile = max(histFiles, key=os.path.getctime)

    return histFile


# HIC SUNT DRACONE
# BEWARE THOSE WHO CONTINUE READING
# THERE IS UGLY CODE AHEAD

def readFile(): 

    histFile = getHistFile() # Let's get the filepath


    coll = "" # we're gonna be collecting data to this later


    # Lets read this binary file
    with open(histFile,"rb") as f: 

        byte = f.read(1)

        while byte != b"":
            byte = f.read(1)
            res = parseByte(byte) # Here we send it to a "parser", it was supposed to do some clever things
                                  # but all it really does is check if the byte is a printable letter or not
            try:
                coll = coll + res # Why is there a try except ? I do not remember
            except:
                pass

    # Now that we have the data
    # Let's split it up on the "adat" tag

    coll = coll.split("adat")
    songs = [ ] # We're gonna be collecting the song here

    for line in coll: # for each section split by the "adat" tag

        if songPathW in line: # If "C:\seraP4th" in this example is found
            
            # My one-off usecase was just for wav files, I added this s**tfix to pretend all 
            # file types are .wav and continue parsing 
            for form in [ ".mp3",".ogg",".alac ",".flac",".aif",".wl.mp3",".mp4",".m4a",".aac" ]:
                line = line.replace(form,".wav")
    

            # yubb, we split on the ".wav" and select the first entry
            songFile = line.split(".wav")[0]
            # Split it by the windows filepath
            songFileName = songFile.split("\\")
            # Select the last one, which is just the filename without the format
            songFileName = songFileName[-1]
            # and we add it to the list
            songs.append(songFileName)

    
    return songs # return a list with all song Names


def printer(msg,newLine): # This was essentially a debug function I forgot to delete

    return # Yeah .....

    if newLine:
        print(msg)
    else:
        print(msg,end='')


def parseByte(byte): # Now we enter the truly ugly stuff
    # here we recieve each individual byte from the session file
    # and go through way to much logic to check if it's a printable character
    # was gonna try and decode the format itself but I got lazy
    # and did the "C:\seraP4th" stuff instead

    
    # let's decode it 
    x = byte.decode("Latin1")

    try: # never fails ...
        # I don't remember if this needs to be done
        y = x.encode("utf-16")
        y = y.decode("utf-16")
    except:
        print("fuuuuuu")
        return

    # ------------------ Begin - Code I could delete 
    # Most common non-character bytes, was trying to
    # find the pattern in them before I decided to ... not
    if byte == b'\x00':
        return 

    if byte == b'\x01':
        printer("-01|",False)
        return 

    if byte == b'\x04':
        printer("-04|",False)
        return 

    if byte == b'\x08':
        printer("-08|",False)
        return
    if byte == b'\x12':
        printer("-12|",False)
        return

    # ------------------ END   - Code I could delete

    # If it can't be decoded as a standard character, ignore it 
    if "\\x" in str(byte):
        f = str(byte)
        f = f.split("x")[1]
        f = f[:-1]
        printer("-_-" + f + "|",False)
        return

    printer(y,False)
    # Return the character if it's a printable character
    return(y)



def helpText():
    print()
    print(" Usage is:")
    a = sys.argv[0]
    b = a + " --data"
    msgLen = len(b) + 5
    print(" " + a.ljust(msgLen) + "       To run the Flask server")
    print(" " + b.ljust(msgLen) + "       To return the data as a list") 
    print()









# Super avanced CLI 
# No argument = run flask
# argument ->
#           if data, return data
#           else: return help

argCount = len(sys.argv)

if argCount == 1:
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        data = readFile()
        return str(data)


    app.run(host='0.0.0.0', port=8080)


elif argCount == 2:
    arg = sys.argv[1] 

    if "data" in arg:
        data = readFile()
        print(data)

    else:
        helpText()
        exit()



