# jsrl_scraper
Web scraper for jetsetradio.live, as [@SleepyLark](https://github.com/sleepylark) will be away for some time

usage: jsrl_scraper.py [-h] [-v [VERBOSE [VERBOSE ...]]] [-stationList [STATIONLIST [STATIONLIST ...]]]
                       [-musicList [MUSICLIST [MUSICLIST ...]]] [-radio [RADIO [RADIO ...]]]
                       [-tv [TV [TV ...]]] [-graffiti [GRAFFITI [GRAFFITI ...]]]
                       [-wallpaper [WALLPAPER [WALLPAPER ...]]] [-all [ALL [ALL ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -v [VERBOSE [VERBOSE ...]]
                        Print verbose while running
  -stationList [STATIONLIST [STATIONLIST ...]]
                        Print a list of stations
  -musicList [MUSICLIST [MUSICLIST ...]]
                        Print a list of songs; Given a station name
  -radio [RADIO [RADIO ...]]
                        Download all music & icons from a radio station; pass a file with station names
                        to download more than one station
  -tv [TV [TV ...]]     Download all TV videos; (Warning this takes some time and about 70GB)
  -graffiti [GRAFFITI [GRAFFITI ...]]
                        Download all default graffiti from the wall;
  -wallpaper [WALLPAPER [WALLPAPER ...]]
                        Download wallpaper;
  -all [ALL [ALL ...]]  Download Everything (make sure you have enough space ~100GB);


Example to download everything:

    python jsrl_scraper.py -all
