#!/usr/bin/env sh
docker network create -d bridge rabbit_net
docker run -d --network=rabbit_net --name rabbit rabbitmq