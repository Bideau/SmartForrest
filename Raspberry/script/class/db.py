#!/usr/bin/python
# -*- coding: utf-8 -*-

class Probe:
    def __init__(self, identifier, probeName):
        self.id = identifier;
        self.name = probeName;

    def getId(self):
        return self.id

    def getBaliseItem(self):
        return self.name


class Monitoring:
    def __init__(self, identifier, monitoringDate, sensorValue, probeId):
        self.id = identifier
        self.date = monitoringDate
        self.sensor = sensorValue
        self.idProbe = probeId

    def getId(self):
        return self.id

    def getDate(self):
        return self.date

    def getSensorValue(self):
        return self.sensor

    def getIdProbe(self):
        return self.idProbe

    def getOzone(self):
        return self.sensor.get("ozone")

    def getTemperature(self):
        return self.sensor.get("temperature")

    def getHygrometry(self):
        return self.sensor.get("hygrometry")

    def getHumidity(self):
        return self.sensor.get("humidity")
