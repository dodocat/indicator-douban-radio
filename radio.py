#coding=utf-8
from api import Api
import json
import pygst
pygst.require("0.10")
import gst
import sys

class Radio:

    def __init__(self):
        """docstring for __init__"""
        print "init radio"
        self.__api = Api()
        self.__plist = []
        self.__index = 0
        self.channel = 0
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_state(gst.STATE_NULL)
        __bus = self.player.get_bus()
        __bus.enable_sync_message_emission()
        __bus.add_signal_watch()
        __bus = gst.Pipeline().get_bus()
        #__bus.connect("message::tag", self.__on_message)
        #__bus.set_sync_handler(self.__on_message)
        __bus.add_watch(self.__on_message)
        self.__log = open('test.log', 'w')
    def __on_message(self, bus, msg):
        mtype = msg.type
        self.__log.writelines("type: " + str(msg.type) + "\n")
        self.__log.flush()

        if mtype == gst.MESSAGE_EOS:
            self.next()
        elif mtype == gst.MESSAGE_ERROR:
            #self.player.set_state(gst.STATE_NULL)
            self.next()
        return gst.BUS_PASS
    def __play(self):
        self.player.set_state(gst.STATE_NULL)
        self.player.set_property('uri', self.__plist[self.__index]['url'])
        self.player.set_state(gst.STATE_PLAYING)
 
    def next(self):
        """ play next song """
        if self.__index >= len(self.__plist):
            chl = self.__api.get_new_playlist(self.channel)
            chl = json.loads(chl)
            if chl['r'] is 0:
                self.__plist = chl['song']
                self.__index = 0
        song = self.__plist[self.__index]
        print song["title"] + " by " + song["artist"]
        self.__play()
        self.__index += 1
    def skip(self):
        """ When user skip current song song get a new list 
            TODO
        """
        self.next()

    def delete(self):
        """ delete song current playing """
        self.skip()
        log.v("delete song")

    def pause(self):
        """ pause play """
        log.v("paused")
    
    def loop(self, isloog):
        """single song loop"""
        log.v("looping")

    def heart(self):
        """mark current song heart"""
        log.v("heart")

    def favor(self, cid=None):
        """ mark channel as favorite channel """
        log.v("channel " + cid + " favorite channels ")

    def get_channels(self):
        """ get channels """
        return self.__api.get_channels() 

    def get_song(self):
        """current song"""
        song = None
        return song
    def login(self, name, password):
        result = self.__api.do_login(name, password)

if __name__ == "__main__":
    radio = Radio()
    if len(sys.argv) is 1 and sys.argv[0] == '--login':
        name = raw_input("Who were you?")
        password = getpass.getpass("the proud lord say")
        radio.login(name, password) 
    radio.next()
    cmd = raw_input("Enter")
    while (cmd != "q"):
        if cmd == "n":
            radio.skip()
        cmd = raw_input("As you wish my Lord:")
    
