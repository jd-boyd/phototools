#!/bin/bash

echo $@

for d in $@;
do
    if [ -d $d ];
    then
        echo Building $d...
        pushd $d
        bash ../../build.sh
        popd
    else
        echo $d isn\'t a directory to build.
    fi
done