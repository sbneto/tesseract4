#!/usr/bin/env bash


for DIR in $(find . -mindepth 1 -maxdepth 3 -not -path '*/\.*' -type d  -not -path '*/\.*'); do
    TAG=${DIR#\./}
    TAG=${TAG//\//-}
    docker pull sbneto/tesseract4:$TAG
    docker build -t sbneto/tesseract4:$TAG --cache-from sbneto/tesseract4:$TAG $DIR
done
