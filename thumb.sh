if [[ -d thumbs ]] ; then echo Preview Director exists ; else mkdir thumbs ; fi

for f in `ls full_size/*.[jJ][pP][gG]` ; do echo working on $f ; convert $f -scale 200x150 thumbs/thumb.`basename $f` ; done
