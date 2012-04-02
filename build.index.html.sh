      touch index.html ;               
      for f in `ls full_size/` ; 	
	do 
	echo "<a href=\"preview/$f\"><img src=\"thumbs/thumb.$f\" /></a>" >> index.html;       
      done ;       
      
