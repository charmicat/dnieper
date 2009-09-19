'''
Created on 22/06/2009

@author: talto
'''

import os
import string
import MP3Info
import stagger
from stagger.id3 import *
import mp3

class Entity:

    def __init__(self, href, text="", is_new="", info=None):
        self.href = href
        self.text = text
        self.is_new = is_new
        self.info = info

            
    def __repr__(self):
        return self.text

class FileInfo:
    def __init__(self, fullpath):
        
        tag = stagger.read_tag(fullpath)
        
        self.title = tag.title
        self.artist = tag.artist
        self.track = tag.track
        self.year = tag.date
        self.comment = tag.comment
        self.composer = tag.composer
        self.album = tag.album
        self.disc = tag.disc
        self.genre = tag.genre
        self.encoder = self.duration = self.filesize = None
        self.bitrate = self.samplerate = self.mode = self.mode_extension = None
        
        info = mp3.mp3info(fullpath)
        

class FileInfoOld:
    """Grab as much info as you can from the file given"""
    def __init__(self, fullpath):
        
        base, ext = os.path.splitext(fullpath)
        ext = ext.lower()

        info = MP3Info.MP3Info(open(fullpath, 'rb'))
        self.__dict__.update(info.__dict__)
        self.total_time = info.mpeg.total_time;
        self.filesize = info.mpeg.filesize2
        self.bitrate = int(info.mpeg.bitrate)
        self.samplerate = info.mpeg.samplerate / 1000
        self.mode = info.mpeg.mode
        self.mode_extension = info.mpeg.mode_extension

      
        if self.total_time > 3600:
            self.duration = '%d:%02d:%02d' % (int(self.total_time / 3600),
                                          int(self.total_time / 60) % 60,
                                          int(self.total_time) % 60)
        elif self.total_time > 60:
            self.duration = '%d:%02d' % (int(self.total_time / 60),
                                     int(self.total_time) % 60)
        else:
            self.duration = '%02d' % int(self.total_time)
            