#!/usr/bin/env python

# part of example from https://kubernetes.io/docs/tasks/job/coarse-parallel-processing-work-queue/
# https://raw.githubusercontent.com/kubernetes/website/master/content/en/examples/application/job/rabbitmq/worker.py

# Just prints standard out and sleeps for 10 seconds.
import sys
import time
print("Processing " + sys.stdin.readlines()[0])
time.sleep(10)
