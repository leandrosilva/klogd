# klogd

Klogd is a simple program to stream [Syslog](http://www.syslog.org) messages to a [Kafka](http://incubator.apache.org/kafka) server.

## Getting Started

### 1) Make sure you have Kafka up and running properly

* [Kafka - Quick Start](http://incubator.apache.org/kafka/quickstart.html)

### 2) Install klogd

    $ git clone git@github.com:leandrosilva/klogd.git
    $ cd klogd
    $ python setup.py install

[Setuptools](http://pypi.python.org/pypi/setuptools) is going to install klogd and its dependencies as well:

* Twisted
* PyParsing
* PyKafka

### 3) Configure Syslog messages routing

On Mac OS X, for example, you have to edit /etc/syslog.conf to include:

    *.info;authpriv,remoteauth,ftp,install,internal.none  @127.0.0.1:1514

### 4) Re-launch Syslog daemon to reflex the new configuration

On Mac OS X, for example, you have to:

    $ launchctl unload /System/Library/LaunchDaemons/com.apple.syslogd.plist
    $ launchctl load /System/Library/LaunchDaemons/com.apple.syslogd.plist

### 5) Start klogd

    $ KAFKA_HOST=127.0.0.1 KAFKA_PORT=9092 klogd 

If you don't provide Kafka environment variables, klogd is going to use defaults:

* **Host** - 127.0.0.1
* **Port** - 9092

### 6) Test it now!

At one terminal:

    $ python tests/kafka_consumer.py

And at another:
    
    $ logger -p local0.info -t test.app "blah blah blah info info info"
    
## Copyright

Copyright (c) 2012 Leandro Silva <leandrodoze@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
