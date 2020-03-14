#!/usr/bin/env sh
docker build -t http_new_task .
docker run --network=rabbit_net --rm -p 8080:8080 http_new_task