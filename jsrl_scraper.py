# JetSetRadio.live Scrapper
# 3/24/2021 by Daniel McDonough
# For Preservation uses only,

import xml.etree.ElementTree as xml
import shutil
import tempfile
import urllib.request
import urllib.parse
import os
import argparse
import requests  # to get image from the web

jsrl_src = "https://jetsetradio.live/radio/stations/"
list_src = "/~list.js"
tv_src = "https://jetsetradio.live/tv/APP/preloader/retrieveTotalFilesAndFilesList.php"
wall_src = "https://jetsetradio.live/wall/APP/editor/library/"
wallpaper_src = "https://jetsetradio.live/wallpaper/images/wallpaper"

def downloadTV(xmlfile):
    # create element tree object
    tree = xml.parse(xmlfile)
    folder = "./tv"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # get root element
    root = tree.getroot()
    for idx,child in enumerate(root):
        print(child.text)
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
                print(link + vid + ".mp4")
                try:
                    urllib.request.urlretrieve(link + vid + ".mp4", filename=output_folder)
                except:
                    print("Could not find "+video)

def downloadWall(cap=241):
    folder = "./wall/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    for img in range(1, cap):
        link = wall_src + str(img) + ".png"
        output_folder = folder + str(img) + ".png"
        downloadImage(link, output_folder)


def downloadImage(link,output_folder,fn):
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(link, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(fn, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image successfully Downloaded: ', output_folder)
    else:
        print('Image Couldn\'t be retrieved: ' + link)


def downloadRadio(station):
    # make source folder
    folder = "./"+station
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Download wallpapers icons etc:
    icon = jsrl_src + station + "/images/icon.png"
    downloadImage(icon, folder,'icon.png')
    desc = jsrl_src + station + "/images/description.png"
    downloadImage(desc, folder,'description.png')
    wallpaper = jsrl_src + station + "/images/wallpaper.jpeg"
    downloadImage(wallpaper, folder,'wallpaper.jpeg')
    wallpaper = jsrl_src + station + "/images/wallpaper.jpg"
    downloadImage(wallpaper, folder,'wallpaper.jpg')



    # get music list script
    js_url = jsrl_src + station + list_src
    with urllib.request.urlopen(js_url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
    # Read each line of JS Script
    lines = []
    with open(tmp_file.name) as html:
        for line in html:
            lines.append(line.rstrip())

    # Get to the point with the music tracks
    try:
        indx = lines.index("//TRACKS")
    except:
        indx = 0

    # for each music track...
    for line in range(indx+1,len(lines),1):
        # check if it is a music track
        linecheck = lines[line].split(" = ")
        if len(linecheck) == 2:

            # track name is set from right side of the equals sign
            songname = linecheck[1]
            # clean up song title from quotes and ;
            cleansong = songname[:-2]
            cleansong = cleansong[1:]

            # download song
            output_folder = folder+"/"+cleansong+".mp3"

            #Only download if new song
            if not os.path.isfile(output_folder):

                print("Downloading: "+jsrl_src + station + "/" + urllib.parse.quote(cleansong) + ".mp3")
                urllib.request.urlretrieve(jsrl_src+station+"/"+urllib.parse.quote(cleansong)+".mp3",filename=output_folder)


def DownloadWallpaperImages():
    for img in range(1, 13):
        link = wallpaper_src + str(img) + ".gif"
        output_folder = "./wallpaper/wallpaper" + str(img) + ".gif"
        downloadImage(link, output_folder)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', help="Download all music and images from a radio station; pass a file with station names to download more than one station ", action='store', dest='radio', nargs='*', type=str, required=False)
    parser.add_argument('-t', help="Download all TV videos; (Warning this takes some time and about 70GB) ", action='store', dest='tv', nargs='*', type=str, required=False)
    parser.add_argument('-w', help="Download all default images from the wall;  ", action='store', dest='wall', nargs='*', type=str, required=False)
    parser.add_argument('-wallpaper', help="Download wallpaper;  ", action='store', dest='wallpaper', nargs='*', type=str, required=False)

    args = parser.parse_args()
    if args.radio is not None:
        for station in args.radio:
            if os.path.isfile(station):
                with open(station) as stationlist:
                    for line in stationlist:
                        downloadRadio(line[:-1])
            else:
                downloadRadio(station)

    if args.tv is not None:
        with urllib.request.urlopen(tv_src) as response:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
        downloadTV(open(tmp_file.name))

    if args.wall is not None:
        downloadWall()

    if args.wallpaper is not None:
        DownloadWallpaperImages()

if __name__ == '__main__':
    main()

exit()

