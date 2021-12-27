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

# Loop on arguments (files)
for arg in sys.argv[1:] :

    # Do nothing of dirs
    if os.path.isdir(arg) :
        continue

    if arg.lower().endswith("cr2"):
        ret = check_output(["dcraw", "-v", "-i", arg])
        date = dict([tuple([f.split(":")[0], ":".join(f.split(":")[1:])])
                     for f in ret.split("\n") if f])["Timestamp"].strip()
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

        date = datetime(*(time.strptime(date, "%Y:%m:%d %H:%M:%S")[0:6]))

    timestamp = int(time.mktime(date.timetuple()))

    # Some traces
    print("File:%s - Ts:%s " % (arg, timestamp))
    print("File:%s - DateTime:%s " % (arg, date))

    # Change the date
    os.utime(arg, (timestamp, timestamp))
