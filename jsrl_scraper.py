#!/bin/python
# JetSetRadio.live Scraper
# 3/24/2021 by Daniel McDonough
# 9/05/2021 - added regex quick look up


import xml.etree.ElementTree as xml
import shutil
import tempfile
import urllib.request
import urllib.parse
import os
import argparse
import requests  # to get image from the web
import re

isVerbose = [False]
jsrl_url = "https://jetsetradio.live/"
jsrl_src = jsrl_url+"radio/stations/"
list_src = "/~list.js"
tv_src = jsrl_url+"tv/APP/preloader/retrieveTotalFilesAndFilesList.php"
wall_src = jsrl_url+"wall/APP/editor/library/"
wallpaper_src = jsrl_url+"wallpaper/images/wallpaper"


# Get the current JSRL stations
def getStations():
    stationList = []
    resp = requests.get(jsrl_url)
    # check if request was successful
    if resp.status_code == 200:
        # get regex string
        decoded = resp.content.decode("utf-8")
        regex = re.compile('(.*)<script src="radio/stations/(.*)/~list.js"></script>(.*)')
        reg = regex.findall(decoded)
        if reg is not None:
            # print stations
            for station in reg:
                stationList.append(station[1])
        else:
            print("ERROR: No stations found")
            exit(1)
    else:
        print("ERROR: Jetsetradio.live is down!")
        exit(1)
    return stationList

# Get each song in a given station
def getMusicList(station):
    musicList = []
    url = jsrl_src+station+list_src
    resp = requests.get(url)
    if resp.status_code == 200:
        # get regex string
        decoded = resp.content.decode("utf-8")
        regex = re.compile('(.*)this\[stationName\+\'_tracks\'].length] = \"(.*)\";')
        reg = regex.findall(decoded)
        if reg is not None:
            # print stations
            for song in reg:
                musicList.append(song[1])
        else:
            print("ERROR: No songs found in " + str(station))
            exit(1)
    else:
        print("ERROR: Jetsetradio.live is down!")
        exit(1)
    return musicList

# download TV mp4s
def downloadTV():
    with urllib.request.urlopen(tv_src) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)

    xmlfile = open(tmp_file.name)
    # create element tree object
    tree = xml.parse(xmlfile)
    folder = "./tv"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # get root element
    root = tree.getroot()
    for idx,child in enumerate(root):
        if(child.text is not None):
            x = child.text.split('"')
            movies = []
            for text in x:
                if '[' not in text and ',' not in text and ']' not in text:
                    movies.append(text)

            for video in movies:

                folder = "./tv/ch"+str(idx)
                if not os.path.exists(folder):
                    os.makedirs(folder)

                link = "https://jetsetradio.live/tv/APP/videoplayer/ch"+str(idx)+"/"
                output_folder = folder+"/"+video+".mp4"
                vid = urllib.parse.quote(video)
                if isVerbose:
                    print("Downloading: "+link + vid + ".mp4")
                try:
                    urllib.request.urlretrieve(link + vid + ".mp4", filename=output_folder)
                except:
                    print("Could not find "+video)

# download wall images
def downloadWall():
    folder = "./wall/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    img = 1
    while True:
        link = wall_src + str(img) + ".png"
        output = str(img) + ".png"
        res = downloadFile(link, folder, output)
        if res == 0:
            img += 1
        else:
            break


# download a single file
def downloadFile(link,output_folder,fn):
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(link, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(output_folder+fn, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        if isVerbose:
            print('File successfully Downloaded: ', output_folder+fn)
        return 0
    else:
        print('File Couldn\'t be retrieved: ' + link)
    return 1



def downloadRadio(station):
    # make source folders
    folder = "./"+station+"/"
    imgfolder = folder+"/images/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(imgfolder):
        os.makedirs(imgfolder)

    # Download wallpapers icons etc:
    icon = jsrl_src + station + "/images/icon.png"
    downloadFile(icon, imgfolder,'icon.png')
    desc = jsrl_src + station + "/images/description.png"
    downloadFile(desc, imgfolder,'description.png')
    wallpaper = jsrl_src + station + "/images/wallpaper.jpg"
    if 1 == downloadFile(wallpaper, imgfolder,'wallpaper.jpg'):
        # sometimes stations have jpeg not jpg
        wallpaper = jsrl_src + station + "/images/wallpaper.jpeg"
        downloadFile(wallpaper, imgfolder,'wallpaper.jpeg')


    list =  jsrl_src + station + "/~list.js"
    downloadFile(list,folder,'~list.js')

    musicList = getMusicList(station)

    # for each music track...
    for song in musicList:
        # download song
        output_folder = folder+"/"+song+".mp3"

        #Only download if new song
        if not os.path.isfile(output_folder):
            if isVerbose:
                print("Downloading: "+jsrl_src + station + "/" + urllib.parse.quote(song) + ".mp3")
            urllib.request.urlretrieve(jsrl_src+station+"/"+urllib.parse.quote(song)+".mp3",filename=output_folder)


def DownloadWallpaperImages():
    if not os.path.exists("./wallpaper"):
        os.makedirs("./wallpaper")
    for img in range(1, 13):
        link = wallpaper_src + str(img) + ".gif"
        output_folder = "./wallpaper/"
        downloadFile(link, output_folder,"wallpaper"+str(img) + ".gif")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', help="Print verbose while running", action='store', dest='verbose',
                        nargs='*', type=str, required=False)
    parser.add_argument('-stationList', help="Print a list of stations", action='store', dest='stationList',
                        nargs='*', type=str, required=False)
    parser.add_argument('-musicList', help="Print a list of songs; Given a station name", action='store',
                        dest='musicList', nargs='*', type=str, required=False)
    parser.add_argument('-radio', help="Download all music & icons from a radio station; pass a file with station names to download more than one station", action='store', dest='radio', nargs='*', type=str, required=False)
    parser.add_argument('-tv', help="Download all TV videos; (Warning this takes some time and about 70GB) ", action='store', dest='tv', nargs='*', type=str, required=False)
    parser.add_argument('-graffiti', help="Download all default graffiti from the wall;  ", action='store', dest='graffiti', nargs='*', type=str, required=False)
    parser.add_argument('-wallpaper', help="Download wallpaper;  ", action='store', dest='wallpaper', nargs='*', type=str, required=False)
    parser.add_argument('-all', help="Download Everything (make sure you have enough space);  ", action='store', dest='all', nargs='*',
                        type=str, required=False)
    args = parser.parse_args()


    if args.verbose is not None:
        isVerbose[0] = True

    # get the current list of stations
    if args.stationList is not None:
        print(getStations())

    # Get the track list of stations
    if args.musicList is not None:
        for station in args.musicList:
            print(getMusicList(station))

    # Download a whole station
    if args.radio is not None:
        for station in args.radio:
            if os.path.isfile(station):
                with open(station) as stationlist:
                    for line in stationlist:
                        downloadRadio(line[:-1])
            else:
                downloadRadio(station)

    # Download the Tv
    if args.tv is not None:
        downloadTV()

    # Download Graffiti
    if args.graffiti is not None:
        downloadWall()

    # Download Wallpaper
    if args.wallpaper is not None:
        DownloadWallpaperImages()

    # Download Everything
    if args.all is not None:
        stations = getStations()
        for station in stations:
            downloadRadio(station)
        downloadWall()
        DownloadWallpaperImages()
        downloadTV()


    exit(0)

if __name__ == '__main__':
    main()


