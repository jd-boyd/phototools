mkdir preview
for f in `ls full_size/*.[jJ][pP][gG]` ; do echo working on $f ; convert $f -scale 800x600 preview/`basename $f` ; done
