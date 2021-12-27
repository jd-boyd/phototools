#!/usr/bin/python3

import os, sys, time
from stat import *

import shutil
import argparse

dates = set()
files_map = {}

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)

        if f[0] == ".":
            print("Skipping hidden file: ", f)
            continue

        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
            #print "Skipping:", pathname
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def visitfile(file):
    print('visiting', file)
    if file==sys.argv[0]:
        #Don't do anything with yourself
        return
    ts = os.stat(file)[ST_MTIME]
    time_fmt = "%b %e %R %Y"
    time_str = time.strftime(time_fmt, time.gmtime(ts))
    time_fmt = "%b%02e"
    dir_time_str = time.strftime(time_fmt, time.gmtime(ts))
    print (time_str)
    dates.add(dir_time_str)
    files_map[file]=dir_time_str

def run():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('src', metavar='SRC', type=str,
                        help='an integer for the accumulator')

    parser.add_argument('dest', metavar='DEST', type=str,
                        help='an integer for the accumulator')

    args = parser.parse_args()
    print(args)
#    sys.exit(0)

    if not args.src[-1] == "/":
        args.src += "/"

    if not args.dest[-1] == "/":
        args.dest += "/"

    walktree(args.src, visitfile)

    print(repr(files_map))
    print(repr(dates))

    for d in dates:
        dir_path = args.dest + d
        try:
            mode = os.stat(dir_path)[ST_MODE]
            if S_ISDIR(mode):
                print(d, "already existed.")
            else:
                print(d, "already existed, but is not a directory.")
                sys.exit(-1)
        except FileNotFoundError:
            print("mkdir", dir_path)
            os.mkdir(args.dest+d)

    for f in files_map:
        d = files_map[f]
        path_split = f.split("/")
        filename = path_split[-1]

        full_src_path_file = f
        full_dest_path_file = args.dest + d +  "/" + filename

        print("cp", full_src_path_file, full_dest_path_file)

        shutil.copy2(full_src_path_file, full_dest_path_file)

if __name__ == '__main__':
    run()
