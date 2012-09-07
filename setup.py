# -*- coding: utf-8 -*-
"""
    klogd
    ~~~~~

    It"s a simple program to stream Syslog messages to a Kafka server.

    :copyright: (c) 2012 by Leandro Silva.
    :license: see README.
"""

from setuptools import setup

setup(
        name             = "klog",
        version          = "0.1",

        install_requires = ["twisted", "pyparsing", "pykafka"],
        packages         = ["klog"],
        package_dir      = {"": "lib"},
        
        scripts          = ["klogd"],
        
        author           = "Leandro Silva",
        author_email     = "leandrodoze@gmail.com",
        keywords         = "klog syslog kafka",
        description      = "Klogd is a simple program to stream Syslog messages to a Kafka server",
        url              = "https://github.com/leandrosilva/klogd",
    )
