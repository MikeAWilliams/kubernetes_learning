#!/usr/bin/env sh
docker build -t python_sleep_new_task .
docker run --network=rabbit_net --rm python_sleep_new_task