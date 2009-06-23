import glob
import os.path
import sys

import cherrypy
from cherrypy.lib.static import serve_file
from ezt import Template
from Entities import Entity
from Entities import FileInfo

class Root:
    def index(self, directory = "c:\mp3"):
        html = """<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head>
        <body><h2>Here are the files in the selected directory:</h2>
        <a href="index?directory=%s">Up</a><br />
        """ % os.path.dirname(os.path.abspath(directory))

        dirs = []
        files = []
        
        for filename in glob.glob(directory + '/*'):
            absPath = os.path.abspath(filename)

            if os.path.isdir(absPath):
                dir = Entity("/index?directory=" + absPath, os.path.basename(filename))
                dirs.append(dir)
                html += '<a href="/index?directory=' + absPath + '">' + os.path.basename(filename) + "</a> <br />"
            else:
                if filename.endswith(".mp3"):
                    info = FileInfo(absPath)
                    file = Entity("/download/?filepath=" + absPath, os.path.basename(filename), "", info)
                    files.append(file)
                    
                html += ' <a href="/download/?filepath=' + absPath + '">' + os.path.basename(filename) + "</a> <br />"
                
        html += """</body></html>"""

        mytemplate = Template("templates/default.ezt")
        data = {"title":"Dnieper Streaming Server",
                "links":"loljuden",
                "pictures":{},
                "subdirs":dirs,
                "display-recursive":"",
                "songs":files}
        
        import StringIO
        
        tmpl = StringIO.StringIO()
        mytemplate.generate(tmpl, data)
        
        text = tmpl.getvalue()
        tmpl.close()

        return text
    
    index.exposed = True

class Download:
    
    def index(self, filepath):
        return serve_file(filepath, "application/x-download", "attachment")
    index.exposed = True

if __name__ == '__main__':
    conf = {'global': {'tools.decode.encoding':"utf8", 'tools.encode.on':True, 'tools.decode.on':True, 'tools.encode.encoding':"utf8"}}
    root = Root()
    root.download = Download()
    cherrypy.quickstart(root, config = conf)
