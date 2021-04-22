#!/usr/bin/env bash


docker build -t sbneto/tesseract4 -f docker/Dockerfile .
docker build -t sbneto/tesseract4:por -f docker/por.Dockerfile .
docker build -t sbneto/tesseract4:eng -f docker/eng.Dockerfile .
