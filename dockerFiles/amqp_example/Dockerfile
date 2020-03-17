# part of example from https://kubernetes.io/docs/tasks/job/coarse-parallel-processing-work-queue/
# https://kubernetes.io/examples/application/job/rabbitmq/Dockerfile
# Specify BROKER_URL and QUEUE when running
FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y curl ca-certificates amqp-tools python \
       --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
COPY ./worker.py /worker.py

CMD  /usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 /worker.py