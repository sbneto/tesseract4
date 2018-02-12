#!/usr/bin/env bash

docker pull sbneto/tesseract4:python
docker pull sbneto/tesseract4:python-por
docker pull sbneto/tesseract4:python-por-rpc

docker build -t sbneto/tesseract4:python --cache-from sbneto/tesseract4:python python/
docker build -t sbneto/tesseract4:python-por --cache-from sbneto/tesseract4:python-por python/por/
docker build -t sbneto/tesseract4:python-por-rpc --cache-from sbneto/tesseract4:python-por-rpc python/por/rpc/
