# jsrl_scraper
Web scraper for jetsetradio.live, as [@SleepyLark](https://github.com/sleepylark) will be away for some time

usage: 

    python jsrl_scraper.py [-h] [-r [STATION|File of stations]] [-t] [-w ] [-wp]

optional arguments:
  
  
  - -h, --help            show this help message and exit
  
  
  - -r [STATION|File of stations]]
                        Download all music and images from a radio station; pass a file with station names to download
                        more than one station
  
  - -t  Download all TV videos; (Warning this takes some time and about 70GB)
  
  
  - -w   Download all default images from the wall;
  
  
  - -wp  Download all gif wallpaper;

Example to download everything:

    python jsrl_scraper.py -r stations.txt -t -w -wp
