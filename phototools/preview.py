import os, re
import subprocess


def make_previews(path, scale):
    """ Path is thumbs or preview, relative to CWD.
        Scale is a string, like '200x150' or '800x600'
    """

    if os.path.exists(path) and os.path.isdir(path):
        print path.capitalize(), "directory exists"
    else:
        os.mkdir(path)

    for f in os.listdir('full_size'):
        if not f.split('.')[-1].lower() == 'jpg':
            continue
        print "Working on", f 
        cmd = ['convert', os.path.join('full_size', f), '-scale', scale, 'thumbs/thumb.%s' % f]
        print "CMD:", cmd
        ret = subprocess.call(" ".join(cmd), shell=True)
        print "RET:", ret
  #      convert $f -scale 200x150 thumbs/thumb.`basename $f` 


def run_thumb():
    make_previews('thumbs', '200x150')

def run_preview():
    make_previews('preview', '800x600')

