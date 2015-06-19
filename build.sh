if [ -z "$1" ] ; then
  DIR="./"
else
  DIR="$1"
fi

echo Entering ${DIR}
pushd ${DIR}
echo Making dir for originals...
mkdir full_size
echo Moving originals to safe directory...
mv *.jpg *.JPG full_size/
echo Building thumb nails...
pt_thumb
echo Building preview size...
pt_preview
echo Building HTML indexes...
pt_index_html
echo Done.
popd


