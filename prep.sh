#!/bin/bash

cp -av $1 /external_1/photos/dc/2010/ && pushd /external_1/photos/dc/2010/$1 && ../../build.sh && popd
