#! /usr/bin/python3

import os
import requests


# How many files from recent history to show
limit = 3 
selRange = range(1,limit + 1)


# Where to store the output files
outFileDir = "/mnt/c/OBS/songData/"
outSong = outFileDir + "currentSong.txt"
outArtist = outFileDir + "currentArtist.txt"
outData = outFileDir + "currentData.txt"

# Where is the flask service running ?
seraUrl = "http://127.0.0.1:8080"


# This function is the entire selector 
# Get data from flask
# select one song, write it to the output files
def getData():
    r = requests.get(seraUrl)


    data = r.text

    # Very elegant
    data = data.split(",")

    c = 1 # Counter for selection
    os.system('clear') # just nice to have a clean screen

    print()
    print("Select Active song:")
    print()

    songDir = { } # build up a collection to select something from
    
    for d in data[-limit:]:

        # print a line with the song info
        print("  - " + str(c) + "    "   + d)

        songDir[str(c)] = d # create a dictionary keyd by the selection numbers
        c = c + 1 

    # get the user input
    answer = input("Select: ") 

    try:
        answer = int(answer) 
    except:
        print()
        print(" Answer should be an interger")
        return

    if answer in selRange:
        selected = songDir[str(answer)]

        # Since I got lazy with the data format, it had some noise in it 
        selected = selected.replace("'","")
        selected = selected.replace("[","")
        selected = selected.replace("]","")
        selected = selected.strip()

        selectedR = selected # We need a copy of this for the full info file
        selected = selected.split("-") # split the entry on "-"

        if len(selected) == 2: # Given the "correct" format of " Artist - SongName "
            f = open(outArtist, "w") # Write the artist
            f.write(selected[0])
            f.close()

            f = open(outSong, "w")   # Write the song
            f.write(selected[1] + "     ")
            f.close()
        else:
            print(" you gon doofd")   # If the format is not " Artist - SongName ", goofing has been done
            print(" Data not in a 'Artist - Song' format")
            print(" Data recieved was:")
            print(" " + selectedR)
            print()

        f = open(outData, "w") # Regardless of artist/song split. still write out the full info
        f.write(selectedR)
        f.close()


    else: # yeah, if you try to select and invalid number
        print()
        print(" Answer should be between 1 and " + str(limit))
        print(" Your answer was: " + str(answer))
        return

    

def looper():
    getData()
    input("Press enter to do re-read and re-do")
    looper()



looper()
