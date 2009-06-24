'''
Created on 23/06/2009

@author: talto
'''

import tempfile

class Tools:
    
    @staticmethod
    def make_playlist(self, urlList):
        f = tempfile.NamedTemporaryFile(delete = True)
        
        for url in urlList:
            f.write(url + "\n")
        
        return f