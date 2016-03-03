#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The MIT License (MIT)
Copyright (c) 2015 Christophe Aubert
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = "Christophe Aubert"
__version__ = "1.0"


class ProbeData(object):

    """

    """

    def __init__(self):
        self.date = None
        self.ozone = None
        self.temperature = None
        self.groundHumidity = None
        self.airHumidity = None
        self.probe = None

    def setValue(self,probe,date,ozone,temperature,humidity,hygrometry):
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