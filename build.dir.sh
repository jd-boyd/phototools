echo "<html><head><title>Photos for year</title></head><body>" > index.html
for d in `'ls'` ; 
  do
    if [ -d $d ] ; then  
    echo \<a href\="$d/index.html"\>$d\</\>\<br /\> >> index.html ; 
    fi
done
echo "</body></html>" >> index.html

