#!/usr/bin/env sh
docker build -t python_sleep_worker .
docker run --network=rabbit_net --rm --name python_sleep_worker python_sleep_worker