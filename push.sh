#!/usr/bin/env bash


for DIR in $(find . -mindepth 1 -maxdepth 3 -not -path '*/\.*' -type d  -not -path '*/\.*'); do
    TAG=${DIR#\./}
    TAG=${TAG//\//-}
    docker push sbneto/tesseract4:$TAG
done
