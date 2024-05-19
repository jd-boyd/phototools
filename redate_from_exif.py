import sys
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import *
from subprocess import check_output
import time
import os

def get_tag(req, img):
    xf = img._getexif()
    for tag in xf:
        if TAGS.get(tag) == req:
            return xf[tag]
    raise KeyError("%r not found in image" % req)

def line_to_pair(l):
    return [l.split(b":")[0], b":".join(l.split(b":")[1:])]

def dcraw_dict(arg):
    ret = check_output(["dcraw", "-v", "-i", arg])
    ar = [tuple(line_to_pair(f))
                     for f in ret.split(b"\n") if f]
    return dict(ar)

# Loop on arguments (files)
for arg in sys.argv[1:] :

    # Do nothing of dirs
    if os.path.isdir(arg) :
        continue

    if arg.lower().endswith("cr2"):
        dc_date = dcraw_dict(arg)
        date = dc_date[b"Timestamp"].strip().decode('utf-8')
        #Wed Feb 19 19:57:29 2014
        date = datetime(*(time.strptime(date, "%a %b %d %H:%M:%S %Y")[0:6]))
    else:
        # Open the file
        img = Image.open(arg)
        try:
            date = get_tag("DateTimeOriginal", img)
        except Exception as e:
            print("Failed to get DateTimeOriginal on", arg, e)
            continue

        try:
            date = datetime(*(time.strptime(date, "%Y:%m:%d %H:%M:%S")[0:6]))
        except Exception as e:
            print("Failed to parse DateTimeOriginal on ", arg, e)

    timestamp = int(time.mktime(date.timetuple()))

    # Some traces
    print("File:%s - Ts:%s " % (arg, timestamp))
    print("File:%s - DateTime:%s " % (arg, date))

    # Change the date
    os.utime(arg, (timestamp, timestamp))
