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


import threading

class ThEmission(threading.Thread):
    """
    Class thread gérant l'émission des messages
    """

    def __init__(self, connection):
        """
        init

        @param connection:
        """
        super(ThEmission, self).__init__()
        threading.Thread.__init__(self)
        self.connection = connection
        self.msgsended = None

    def run(self):
        while 1:
            # self.msgsended = raw_input('Enter your msg : ')
            # self.connection.send(self.msgsended)
            pass

    def reSendMsg(self):
        """
        Méthode pour renvoyer le message
        """
        self.connection.send(self.msgsended)

    def sendMsg(self, msg):
        """
        Méthode pour envoyé un message

        @param msg:

        """
        self.msgsended = msg
        self.connection.send(self.msgsended)