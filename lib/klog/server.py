# -*- coding: utf-8 -*-
"""
    klogd
    ~~~~~

    It's a simple program to stream Syslog messages to a Kafka server.

    :copyright: (c) 2012 by Leandro Silva.
    :license: see README.
"""

from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol, Factory
from time import strftime
import sys, os, json, kafka

severity = ["emerg", "alert", "crit", "err", "warn", "notice", "info", "debug"]

facility = ["kern", "user", "mail", "daemon", "auth", "syslog", "lpr", "news",
            "uucp", "cron", "authpriv", "ftp", "ntp", "audit", "alert", "at", "local0",
            "local1", "local2", "local3", "local4", "local5", "local6", "local7"]

class Parser(object):
  def __init__(self):
    self.__pattern = self.__build_pattern()
    
  def __build_pattern(self):
    ints = Word(nums)

    # priority
    priority = Suppress("<") + ints + Suppress(">")

    # timestamp
    month = Word(string.uppercase, string.lowercase, exact=3)
    day   = ints
    hour  = Combine(ints + ":" + ints + ":" + ints)
    
    timestamp = month + day + hour

    # hostname
    hostname = Word(alphas + nums + "_" + "-" + ".")

    # appname
    appname = Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + ints + Suppress("]")) + Suppress(":")

    # message
    message = Regex(".*")
  
    # pattern build
    return priority + timestamp + hostname + appname + message
    
  def parse(self, line, (host, port)):
    parsed_line = self.__pattern.parseString(line)

    _priority = parsed_line[0]
    (_facility, _severity) = self.__get_level(_priority)
    
    payload = {}
    payload["priority"]  = _priority
    payload["facility"]  = _facility
    payload["severity"]  = _severity
    payload["timestamp"] = strftime("%Y-%m-%d %H:%M:%S")
    payload["hostname"]  = parsed_line[4]
    payload["hostaddr"]  = host
    payload["hostport"]  = port
    payload["appname"]   = parsed_line[5]
    payload["pid"]       = parsed_line[6]
    payload["message"]   = parsed_line[7]
    
    return json.dumps(payload)
    
  def __get_level(self, priority):
    _priority = int(priority)
    _facility = _priority / 8
    _severity = _priority % 8
    
    return (facility[_facility], severity[_severity])
    
class Receiver(DatagramProtocol):
  def __init__(self):
    self.__parser = Parser()
    self.__kafka = Kafka()
    
  def datagramReceived(self, data, (host, port)):
    payload = self.__parser.parse(data, (host, port))
    self.__kafka.send(payload)
    
class Kafka(object):
  def __init__(self):
    try:
      self.__host = os.getenv("KAFKA_HOST")
      self.__port = int(os.getenv("KAFKA_PORT"))
    except Exception:
      self.__host = "127.0.0.1"
      self.__port = 9092
      
  def send(self, payload):
    producer = kafka.producer.Producer('klog', host=self.__host, port=self.__port)
    message  = kafka.message.Message(payload)
    producer.send(message)
    
# Let's kick off it

def run():
  reactor.listenUDP(1514, Receiver())
  reactor.run()
