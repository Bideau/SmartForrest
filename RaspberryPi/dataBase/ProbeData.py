#!/usr/bin/python
# -*- coding: utf-8 -*-

class ProbeData(object):

    def __init__(self):
        self.date = None
        self.ozone = None
        self.temperature = None
        self.groundHumidity = None
        self.airHumidity = None
        self.probe = None

    def setValue(self,date,ozone,temperature,humidity,hygrometry,probe):
        self.date = date
        self.ozone = ozone
        self.temperature = temperature
        self.airHumidity = humidity
        self.groundHumidity = hygrometry
        self.probe = probe

    def toJson(self):
        _json = ("{" +
                 "probeID" + ":" + str(self.probe) + "," +
                 "date" + ":" + str(self.date) + "," +
                 "ozone" ":" + str(self.ozone) + "," +
                 "temperature" + ":" + str(self.temperature) + "," +
                 "groundHumidity" + ":" + str(self.groundHumidity) + "," +
                 "airHumidity" + ":" + str(self.airHumidity) +
                 "}"
                 )
        return _json