"""
Ubipy Music Player

Dependencies:
pygame
mutagen
easygui

    Ubipy Cross-Platform Free Music Player
    Copyright (C) 2016 Damian Heaton <me@damianheaton.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

name = "Ubipy Music Player"
relt = "LibPlayer"
verid = "0.7.1"
debug = True

import pygame
from pygame.locals import *
from mutagen.id3 import ID3 as id3
from mutagen.mp3 import MP3 as mp3
from mutagen import File as mfile
import sys
import os
import time
import logging
import easygui
import random
import urllib.request
import webbrowser
import src.Legal
import src.Update
import src.Index

src.Legal.printGNU(name)

if debug:
    loglev = logging.DEBUG
else:
    loglev = logging.WARN
log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s',
                              '%d/%m/%Y %H:%M:%S %p')

fh = logging.FileHandler(name + '.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(loglev)
ch.setFormatter(formatter)
log.addHandler(ch)

#log.debug('This message should appear on the console')
#log.info('So should this')
#log.warning('And this, too')

log.debug("========= START =========")

src.Update.update(name, log, verid, "ubipy")

pygame.mixer.init()
pygame.display.init()
pygame.font.init()

volume = 0.75

log.info("Indexing songs... Please wait.")

indexedSongs = src.Index.indexAll()

maxsong = indexedSongs[0]
ogg = indexedSongs[1]
songs = indexedSongs[2]
shuffledSongs = indexedSongs[3]
artists = indexedSongs[4]
artists2 = indexedSongs[5]
albums = indexedSongs[6]
albums2 = indexedSongs[7]

if ogg:
    log.warn("""Ubipy has detected that some of your songs are in an Ogg Vorbis
file format. Unfortunately, Ogg Vorbis (.ogg) are not fully supported (yet), and
as a result, skipping to a specific part of these tracks, viewing the tracks'
lengths, and other track length dependant features will not be available for
these tracks.""")

log.info("Songs available to play: " + str(maxsong + 1))
if maxsong == -1:
    log.critical("""No songs available to play. Please add songs, following this
folder structure:
    |-artist
        |-album
            |-songs""")
    sys.exit("critical error")

## print(songs)
## sys.exit("test")

""" print(rsongs)
print(artists)
print(albums)
print(songs) """

#pygame.display.init()
#pygame.time.init()
#pygame.font.init()
shuffle = False
prev = pygame.transform.scale(pygame.image.load("res/prev.png"), (100, 100))
pause = pygame.transform.scale(pygame.image.load("res/pause-new.png"),
                               (100, 100))
play = pygame.transform.scale(pygame.image.load("res/play.png"), (100, 100))
n3xt = pygame.transform.scale(pygame.image.load("res/next.png"), (100, 100))
back = pygame.transform.scale(pygame.image.load("res/back.png"), (100, 100))
shufflebtn = {
    "True" : pygame.transform.scale(pygame.image.load("res/shuffle-True.png"),
                                    (100, 100)),
    "False" : pygame.transform.scale(pygame.image.load("res/shuffle-False.png"),
                                    (100, 100))
}
font = pygame.font.SysFont("times new roman", 33)
if os.path.isfile("#song.txt"):
    try:
        f = open("#song.txt", "r")
        cursong = songs.index(f.read())
        f.close()
    except:
        log.error("""The song defined in #song.txt does not exist.
Starting from 0.""")
        cursong = 0
else:
    cursong = 0
if os.path.isfile("#songt.txt"):
    f = open("#songt.txt", "r")
    st = float(f.read())
    f.close()
else:
    st = 0.0
startsong = cursong
pygame.mixer.music.set_endevent(USEREVENT)
try: # a few files are m4a, not mp3
    pygame.mixer.music.load(songs[cursong])
except: # file cannot be played - this shouldn't happen. ever.
    log.error("Could not play song:", songs[cursong])
try:
    albumart = mfile(songs[cursong]).tags["APIC:"].data
    with open("albumart.jpg", "wb") as img:
        img.write(albumart)
except:
    albumartf = open("albumart-placeholder.png", "rb")
    albumart = albumartf.read()
    albumartf.close()
    with open("albumart.jpg", "wb") as img:
        img.write(albumart)
if songs[cursong].endswith(".mp3"):
    tracklength = mp3(songs[cursong]).info.length
else:
    tracklength = None
metadata = id3(songs[cursong])
try:
    log.info("SONG #" + str(cursong) + " | Playing " + metadata['TIT2'].text[0]
             + " in " + metadata['TALB'].text[0] + " by "
             + metadata['TPE1'].text[0])
except:
    log.debug("Unable to get metadata for " + songs[cursong] + """.
Basing it off directory tree instead.""")
    log.info("SONG #" + str(cursong) + " | Playing "
             + songs[cursong].split("/")[3].split(".")[0] + " in "
             + songs[cursong].split("/")[2] + " by "
             + songs[cursong].split("/")[1])
pygame.mixer.music.play(0, st)
display = pygame.display.set_mode((1500, 900)) # 135
pygame.display.set_caption(name)
while True:
    posx, posy = pygame.mouse.get_pos()
    try:
        for event in pygame.event.get():
            if event.type == QUIT:
                display.fill((255, 0, 0))
                pygame.display.update()
                if shuffle:
                    song = shuffledSongs[cursong]
                else:
                    song = songs[cursong]
                f = open("#song.txt", "w")
                f.write(song)
                f.close()
                f = open("#songt.txt", "w")
                f.write(str(pygame.mixer.music.get_pos() / 1000 + st))
                f.close()
                pygame.mixer.music.stop()
                pygame.quit()
            elif event.type == USEREVENT:
                st = 0.0
                if cursong < maxsong:
                    cursong += 1
                else:
                    cursong = 0
                if shuffle == True:
                    song = shuffledSongs[cursong]
                else:
                    song = songs[cursong]
                try: # a few files are m4a, not mp3
                    pygame.mixer.music.load(song)
                except: # file cannot be played - this shouldn't happen. ever.
                    log.error("Could not play song:", song)
                try:
                    albumart = mfile(song).tags["APIC:"].data
                    with open("albumart.jpg", "wb") as img:
                        img.write(albumart)
                except:
                    albumartf = open("albumart-placeholder.png", "rb")
                    albumart = albumartf.read()
                    albumartf.close()
                    with open("albumart.jpg", "wb") as img:
                        img.write(albumart)
                if song.endswith(".mp3"):
                    tracklength = mp3(song).info.length
                else:
                    tracklength = None
                metadata = id3(song)
                try:
                    log.info("SONG #" + str(cursong) + " | Now playing "
                             + metadata['TIT2'].text[0] + " in "
                             + metadata['TALB'].text[0] + " by "
                             + metadata['TPE1'].text[0])
                except:
                    log.debug("Unable to get metadata for " + song
                              + ". Basing it off directory tree instead.")
                    log.info("SONG #" + str(cursong) + " | Now playing "
                             + song.split("/")[3].split(".")[0]
                             + " in " + song.split("/")[2] + " by "
                             + song.split("/")[1])
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(0)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if volume < 1:
                        volume += 0.05
                        pygame.mixer.music.set_volume(volume)
                if event.button == 5:
                    if volume > 0:
                        volume -= 0.05
                        pygame.mixer.music.set_volume(volume)
                if event.button == 1:
                    if 885 <= posy <= 900:
                        if tracklength is not None:
                            mpercent = posx / 1500 * 100
                            secs = tracklength / 100 * mpercent
                            st = secs
                            pygame.mixer.music.play(0, secs)
                            # print(mpercent, "%:", mseconds)
                    if 0 <= posx <= 375:
                        if 0 <= posy <= 34:
                            folder = easygui.choicebox("Please enter the artist you\
     wish to listen to.", "Ubipy :: Select artist", artists2)
                            if folder is not None:
                                # IMPORTANT NTS
                                # try: src.Index.indexArtist(folder)
                                indexedSongs = src.Index.indexArtist(folder)
                                maxsong = indexedSongs[0]
                                songs = indexedSongs[1]
                                shuffledSongs = indexedSongs[2]
                                cursong = 0
                                st = 0.0
                                try: # a few files are m4a, not mp3
                                    pygame.mixer.music.load(songs[cursong])
                                except: # file cannot be played - this shouldn't happen. ever.
                                    log.error("Could not play song:", songs[cursong])
                                try:
                                    albumart = mfile(songs[cursong]).tags["APIC:"].data
                                    with open("albumart.jpg", "wb") as img:
                                        img.write(albumart)
                                except:
                                    albumartf = open("albumart-placeholder.png", "rb")
                                    albumart = albumartf.read()
                                    albumartf.close()
                                    with open("albumart.jpg", "wb") as img:
                                        img.write(albumart)
                                if songs[cursong].endswith(".mp3"):
                                    tracklength = mp3(songs[cursong]).info.length
                                else:
                                    tracklength = None
                                metadata = id3(songs[cursong])
                                try:
                                    log.info("SONG #" + str(cursong) + " | Now playing "
                                             + metadata['TIT2'].text[0] + " in "
                                             + metadata['TALB'].text[0] + " by "
                                             + metadata['TPE1'].text[0])
                                except:
                                    log.debug("Unable to get metadata for " + songs[cursong]
                                              + ". Basing it off directory tree instead.")
                                    log.info("SONG #" + str(cursong) + " | Now playing "
                                             + songs[cursong].split("/")[3].split(".")[0]
                                             + " in " + songs[cursong].split("/")[2]
                                             + " by " + songs[cursong].split("/")[1])
                                pygame.mixer.music.set_volume(volume)
                                pygame.mixer.music.play(0)
                        elif 40 <= posy <= 70:
                            album = easygui.choicebox("Please enter the album you\
     wish to listen to.", "Ubipy :: Select album", albums2)
                            if album is not None:
                                album = album.split(", by ")
                                folder = album[1]
                                subfolder = album[0]
                                indexedSongs = src.Index.indexAlbum(folder, subfolder)
                                maxsong = indexedSongs[0]
                                songs = indexedSongs[1]
                                shuffledSongs = indexedSongs[2]
                                cursong = 0
                                st = 0.0
                                try: # a few files are m4a, not mp3
                                    pygame.mixer.music.load(songs[cursong])
                                except: # file cannot be played - this shouldn't happen. ever.
                                    log.error("Could not play song:", songs[cursong])
                                try:
                                    albumart = mfile(songs[cursong]).tags["APIC:"].data
                                    with open("albumart.jpg", "wb") as img:
                                        img.write(albumart)
                                except:
                                    albumartf = open("albumart-placeholder.png", "rb")
                                    albumart = albumartf.read()
                                    albumartf.close()
                                    with open("albumart.jpg", "wb") as img:
                                        img.write(albumart)
                                if songs[cursong].endswith(".mp3"):
                                    tracklength = mp3(songs[cursong]).info.length
                                else:
                                    tracklength = None
                                metadata = id3(songs[cursong])
                                try:
                                    log.info("SONG #" + str(cursong) + " | Now playing "
                                             + metadata['TIT2'].text[0] + " in "
                                             + metadata['TALB'].text[0] + " by "
                                             + metadata['TPE1'].text[0])
                                except:
                                    log.debug("Unable to get metadata for " + songs[cursong]
                                              + ". Basing it off directory tree instead.")
                                    log.info("SONG #" + str(cursong) + " | Now playing "
                                             + songs[cursong].split("/")[3].split(".")[0]
                                             + " in " + songs[cursong].split("/")[2]
                                             + " by " + songs[cursong].split("/")[1])
                                pygame.mixer.music.set_volume(volume)
                                pygame.mixer.music.play(0)
                    elif 900 <= posx <= 1000 and 751 <= posy <= 851:
                        shuffle = not shuffle
                    elif 1000 <= posx <= 1100 and 751 <= posy <= 851:
                        st = 0
                        pygame.mixer.music.play(0)
                    elif 1100 <= posx <= 1200 and 751 <= posy <= 851:
                        st = 0.0
                        if cursong > 0:
                            cursong -= 1
                        else:
                            cursong = maxsong
                        if shuffle == True:
                            song = shuffledSongs[cursong]
                        else:
                            song = songs[cursong]
                        try: # a few files are m4a, not mp3
                            pygame.mixer.music.load(song)
                        except: # file cannot be played - this shouldn't happen. ever.
                            log.error("Could not play song:", song)
                        try:
                            albumart = mfile(song).tags["APIC:"].data
                            with open("albumart.jpg", "wb") as img:
                                img.write(albumart)
                        except:
                            albumartf = open("albumart-placeholder.png", "rb")
                            albumart = albumartf.read()
                            albumartf.close()
                            with open("albumart.jpg", "wb") as img:
                                img.write(albumart)
                        if song.endswith(".mp3"):
                            tracklength = mp3(song).info.length
                        else:
                            tracklength = None
                        metadata = id3(song)
                        try:
                            log.info("SONG #" + str(cursong) + " | Now playing "
                                     + metadata['TIT2'].text[0] + " in "
                                     + metadata['TALB'].text[0] + " by "
                                     + metadata['TPE1'].text[0])
                        except:
                            log.debug("Unable to get metadata for " + song
                                      + ". Basing it off directory tree instead.")
                            log.info("SONG #" + str(cursong) + " | Now playing "
                                     + song.split("/")[3].split(".")[0]
                                     + " in " + song.split("/")[2] + " by "
                                     + song.split("/")[1])
                        pygame.mixer.music.set_volume(volume)
                        pygame.mixer.music.play(0)
                        st = 0
                    elif 1201 <= posx <= 1300 and 751 <= posy <= 851:
                        pygame.mixer.music.pause()
                    elif 1301 <= posx <= 1400 and 751 <= posy <= 851:
                        pygame.mixer.music.unpause()
                    elif 1401 <= posx <= 1500 and 751 <= posy <= 851:
                        st = 0.0
                        if cursong < maxsong:
                            cursong += 1
                        else:
                            cursong = 0
                        if shuffle == True:
                            song = shuffledSongs[cursong]
                        else:
                            song = songs[cursong]
                        try: # a few files are m4a, not mp3
                            pygame.mixer.music.load(song)
                        except: # file cannot be played - this shouldn't happen. ever.
                            log.error("Could not play song:", song)
                        try:
                            albumart = mfile(song).tags["APIC:"].data
                            with open("albumart.jpg", "wb") as img:
                                img.write(albumart)
                        except:
                            albumartf = open("albumart-placeholder.png", "rb")
                            albumart = albumartf.read()
                            albumartf.close()
                            with open("albumart.jpg", "wb") as img:
                                img.write(albumart)
                        if song.endswith(".mp3"):
                            tracklength = mp3(song).info.length
                        else:
                            tracklength = None
                        metadata = id3(song)
                        try:
                            log.info("SONG #" + str(cursong) + " | Now playing "
                                     + metadata['TIT2'].text[0] + " in "
                                     + metadata['TALB'].text[0] + " by "
                                     + metadata['TPE1'].text[0])
                        except:
                            log.debug("Unable to get metadata for " + song
                                      + ". Basing it off directory tree instead.")
                            log.info("SONG #" + str(cursong) + " | Now playing "
                                     + song.split("/")[3].split(".")[0]
                                     + " in " + song.split("/")[2] + " by "
                                     + song.split("/")[1])
                        pygame.mixer.music.set_volume(volume)
                        pygame.mixer.music.play(0)
        display.fill((0, 0, 0))
        try:
            title = font.render("Song: " + metadata['TIT2'].text[0], True,
                                (255, 50, 255))
            album = font.render("Album: " + metadata['TALB'].text[0], True,
                                (255, 50, 255))
            artist = font.render("Artist: " + metadata['TPE1'].text[0], True,
                                 (255, 50, 255))
        except:
            splitdata = songs[cursong].split("/")
            title = font.render("Song: " + splitdata[3].split(".")[0], True,
                                (255, 50, 255))
            album = font.render("Album: " + splitdata[2], True, (255, 50, 255))
            artist = font.render("Artist: " + splitdata[1], True,
                                 (255, 50, 255))
        vol = font.render("Volume: " + str(int(volume * 100)) + "%", True,
                          (255, 50, 255))
        display.blit(title, (0, 750))
        display.blit(album, (0, 784))
        display.blit(artist, (0, 817))
        display.blit(vol, (0, 851))
        display.blit(shufflebtn[str(shuffle)], (900, 751))
        display.blit(back, (1000, 751))
        display.blit(prev, (1100, 751))
        display.blit(pause, (1200, 751))
        display.blit(play, (1300, 751))
        display.blit(n3xt, (1400, 751))
        display.blit(pygame.transform.scale(pygame.image.load("albumart.jpg"),
                                            (750, 750)), (375, 0))
        pygame.draw.rect(display, (255, 50, 255), (0, 0, 375, 34), 4)
        artisttxt = title = font.render("Artist", True, (255, 255, 255))
        pygame.draw.rect(display, (255, 50, 255), (0, 40, 375, 34), 4)
        albumtxt = title = font.render("Album", True, (255, 255, 255))
        if 0 <= posx <= 375:
            if 0 <= posy <= 34:
                pygame.draw.rect(display, (255, 50, 255), (0, 0, 375, 34))
            elif 40 <= posy <= 70:
                pygame.draw.rect(display, (255, 50, 255), (0, 40, 375, 34))
        display.blit(artisttxt, (6, 0))
        display.blit(albumtxt, (6, 40))
        if cursong == startsong:
            minutes = (pygame.mixer.music.get_pos() // 60000) + (int(st) // 60)
            seconds = ((pygame.mixer.music.get_pos() // 1000)
                       + int(st)) - (minutes * 60)
        else:
            minutes = pygame.mixer.music.get_pos() // 60000
            seconds = pygame.mixer.music.get_pos() // 1000 - (minutes * 60)
        if tracklength is not None:
            trackmin = int(tracklength // 60)
            tracksec = int(tracklength - (trackmin * 60))
            playtime = font.render(str(minutes) + ":" + str(seconds) + " / "
                               + str(trackmin) + ":" + str(tracksec), True,
                               (255, 50, 255))
        else:
            playtime = font.render(str(minutes) + ":" + str(seconds), True,
                                   (255, 50, 255))
        display.blit(playtime, (1360, 852))
##        if cursong == startsong:
        minutes = (pygame.mixer.music.get_pos() // 60000) + (int(st) // 60)
        seconds = ((pygame.mixer.music.get_pos() // 1000)
                   + int(st)) - (minutes * 60)
        if tracklength is not None:
            percent = (pygame.mixer.music.get_pos() / 1000
                       + int(st)) / tracklength * 100
##        else:
##            minutes = pygame.mixer.music.get_pos() // 60000
##            seconds = pygame.mixer.music.get_pos() // 1000 - (minutes * 60)
##            percent = (pygame.mixer.music.get_pos() / 1000) / tracklength * 100
        pygame.draw.rect(display, (255, 200, 255), (0, 885, 1500, 15))
        if 885 <= posy <= 900 and tracklength is not None:
            mpercent = posx / 1500 * 100
            if mpercent > percent:
                pygame.draw.rect(display, (255, 0, 255),
                                 (0, 885, (1500 / 100 * mpercent), 15))
            pygame.draw.rect(display, (255, 100, 255),
                             (0, 885, (1500 / 100 * percent), 15))
            if 885 <= posy <= 900:
                if mpercent <= percent:
                    pygame.draw.rect(display, (255, 0, 255),
                                     (0, 885, (1500 / 100 * mpercent), 15))
        elif tracklength is not None:
            pygame.draw.rect(display, (255, 100, 255),
                             (0, 885, (1500 / 100 * percent), 15))
        pygame.display.update()
    except Exception as e:
        log.exception(e)
        break