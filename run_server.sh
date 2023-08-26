#!/bin/bash
apt install docker.io -y
docker pull feel2code/jessiegram:latest
docker run --env-file .env -d -p 80:8000 feel2code/jessiegram