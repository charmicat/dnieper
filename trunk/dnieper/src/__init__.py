'''
Created on 20/06/2009

@author: talto
'''

import ConfigParser
from ezt import Template
import sys

def main ():
    config = ConfigParser.SafeConfigParser()
    config.read("resources/dnieper.cfg")
    dirs = config.items("Sources")
    
    print (config.get("Server", "port"))
    print (dirs)

    mytemplate = Template("templates/default.ezt")
    data = {"title":"fuck this shit"}
    
    mytemplate.generate(sys.stdout, data)


if __name__ == '__main__':
    main()
