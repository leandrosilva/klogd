# -*- coding: utf-8 -*-
"""
    klogd
    ~~~~~

    It's a simple program to stream Syslog messages to a Kafka server.

    :copyright: (c) 2012 by Leandro Silva.
    :license: see README.
"""

#
# This script consumes klog topic from Kafka, for test purpose.
#

import kafka

consumer = kafka.consumer.Consumer("klog")

for message in consumer.loop():
  print "received:", message
  