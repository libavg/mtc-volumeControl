#!/usr/bin/env python
# Copyright (C) 2009
#    Martin Heistermann, <mh at sponc dot de>
#
# appChooser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# appChooser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with appChooser.  If not, see <http://www.gnu.org/licenses/>.

from libavg import avg, Point2D, eventList
from libavg import AVGApp
from libavg.AVGAppUtil import getMediaDir

import alsaaudio
import os


g_player = avg.Player.get()

class Slider(object):
    """value normalized 0-1"""
    def __init__(self, parentNode, pos, onChange = lambda value: None):
        self.__onChange = onChange
        self.__node = g_player.createNode('div', {
            'x': pos.x,
            'y': pos.y,
            })
        parentNode.appendChild(self.__node)
        self.__bgNode = g_player.createNode('image', {
            'href': 'slider_bar.png',
            })
        self.__node.appendChild(self.__bgNode)
        self.__handleNode = g_player.createNode('image', {
            'href': 'slider_handle.png',
            })
        self.__node.appendChild(self.__handleNode)
        self.__bgNode.x += (self.__handleNode.width - self.__bgNode.width)/2

        self.__distY = self.__bgNode.height - self.__handleNode.height

        self.__eventList = eventList.EventList(self.__handleNode,
                source = avg.TOUCH | avg.MOUSE,
                onDown = self._onDown,
                onMotion = self._onMotion,
                maxEvents = 1,
                captureEvents = True)

    def _onDown(self, eventCursor):
        self._startValue = self._value
    def _onMotion(self, eventCursor):
        motionY = eventCursor.getDelta().y
        value = self._startValue + (motionY / self.__distY)
        if value<0:
            value = 0
        if value>1:
            value = 1
        self.setValue(value)

    def setValue(self, val):
        assert val >= 0 and val <= 1
        self._value = val
        self.__handleNode.y = self.__distY * val
        self.__onChange(val)

class VolumeControl(AVGApp):
    multitouch = True
    def __init__(self, parentNode):
        parentNode.mediadir = getMediaDir(__file__)

        bgNode = g_player.createNode('image', {
            'href': "bgpixel.png"})
        bgNode.size = parentNode.size
        parentNode.appendChild(bgNode)

        self.__mixer = alsaaudio.Mixer()
        def setVolume(val):
            val = 1 - val
            self.__mixer.setvolume(int(100 * val))

        schieberWidth = 100
        self.__schieber = Slider(parentNode,
                pos = Point2D(300,10),
                onChange = setVolume)

        self.__audioNode = g_player.createNode('sound', {
            'href': os.path.join(getMediaDir(__file__), 'test.wav')})
        parentNode.appendChild(self.__audioNode)
        def onFinish():
            self.__isPlaying = False
        self.__audioNode.setEOFCallback(onFinish)
        self.__isPlaying = False

        testNode = g_player.createNode('words', {
            'text': 'VOLUME',
            'x': 600,
            'y': 50,
            'size': 150,

            })
        parentNode.appendChild(testNode)
        #testNode.setEventHandler(avg.CURSORDOWN,
        #        avg.MOUSE | avg. TOUCH, self._onClickPlay)
        exitNode = g_player.createNode('words', {
            'text': 'EXIT',
            'x': 600,
            'y': 450,
            'size': 150,

            })
        parentNode.appendChild(exitNode)
        exitNode.setEventHandler(avg.CURSORDOWN,
                avg.MOUSE | avg. TOUCH, lambda e: self.leave())



    def _onClickPlay(self, event):
        if self.__isPlaying:
            return
        self.__audioNode.stop()
        self.__audioNode.play()
        self.__isPlaying = True

    def _enter(self):
        volume = float(self.__mixer.getvolume()[0])
        print "setting", volume
        self.__schieber.setValue(1 - (volume/100))

if __name__ == '__main__':
    VolumeControl.start(resolution = (1280,720))


