#!/usr/bin/env bash

docker build -t sbneto/tesseract4:python python/
docker build -t sbneto/tesseract4:python-por python/por/
docker build -t sbneto/tesseract4:python-por-rpc python/por/rpc/