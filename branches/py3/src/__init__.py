'''
Created on 20/06/2009

@author: talto
'''

import configparser
from webserver import Root, Download, Sources
import cherrypy

def parse_config():
    dirs = cherrypy.request.app.config['Sources']
    
    print (dirs)

def main ():
    sources = Sources()
    sources.root = Root()
    sources.root.download = Download()
    cherrypy.quickstart(sources, config = "resources/dnieper.cfg")


if __name__ == '__main__':
    main()
