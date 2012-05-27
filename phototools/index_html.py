#!/usr/bin/python

import re, os

findParmRe = re.compile("(\$.)")

top="""
<html>
<head>
<title>$t</title>
<link rel="stylesheet" type="text/css" href="../../style.css"
      title="default"/>

<script type="text/javascript" src="../../addLoadEvent.js"></script>

<script type="text/javascript" src="../../getElementsBySelector.js"></script>
<script type="text/javascript" src="../../imagebox.js"></script>
</head>
<body>

<h1>$t</h1>

<div class="thumbs">
"""

imgLine = """
  <a href="preview/$i" title="$i"><img src="thumbs/thumb.$i" /></a>
"""

bottom="""</div>

<div><img id="largeImg" src="preview/$f" alt="Large image" /></div>

<div id="desc">$f</div>

</body>
</html>"""


def run():
    f= open("index.html", "w")

    pList=[]
    for p in os.walk("./full_size/"):
        pList = p[2]

    pList.sort()

    lRe = re.compile("\$i")
    bRe = re.compile("\$f")

    f.write(top)
    pFirst=None
    for p in pList:
        if not pFirst:
            pFirst=p
        l = lRe.sub(p, imgLine)
        f.write(l + "\n")

    f.write(bRe.sub(pFirst,bottom))
    f.close()
