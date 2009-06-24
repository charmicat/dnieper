import glob
import os.path
import sys
import StringIO
import cherrypy

from cherrypy.lib.static import serve_file
from ezt import Template
from Entities import Entity, FileInfo
import Tools

class Root:
    def index(self, directory = "c:\mp3"):
        dirs = []
        files = []
        
        for filename in glob.glob(directory + '/*'):
            absPath = os.path.abspath(filename)

            if os.path.isdir(absPath):
                dir = Entity("/root?directory=" + absPath, os.path.basename(filename))
                dirs.append(dir)
            else:
                if filename.endswith(".mp3"):
                    info = FileInfo(absPath)
                    file = Entity("/root/download/?filepath=" + absPath, os.path.basename(filename), "", info)
                    files.append(file)
                elif filename.endswith(".m3u"):
                    print "im hier"
                    
                    f = Tools.make_playlist("/root/download/?filepath=" + absPath)
                    return serve_file(f.name, "application/x-download", "attachment")
                    
        mytemplate = Template("templates/default.ezt")
        data = {"title":"Dnieper Streaming Server",
                "links":"loljuden", # quebrar o path ate o root
                "pictures":{},
                "subdirs":dirs,
                "display-recursive":"",
                "songs":files}
        
        tmpl = StringIO.StringIO()
        mytemplate.generate(tmpl, data)
        
        text = tmpl.getvalue()
        tmpl.close()

        return text
    
    index.exposed = True
    
class Sources:
    def index(self):
        dirs = []
        directories = cherrypy.request.app.config['Sources']
        
        for dirCfg in directories.values():
            toks = dirCfg.split("(")
            dirPath = toks[0].strip()
            dirLabel = toks[1].strip(")")
            
            absPath = os.path.abspath(dirPath) 

            if os.path.isdir(absPath):
                dirObj = Entity("/root?directory=" + absPath, dirLabel)
                dirs.append(dirObj)
            else:
                #retornar erro! diretorios devem existir!
                pass
                    
        mytemplate = Template("templates/default.ezt")
        data = {"title":"Dnieper Streaming Server",
                "links":"Sources",
                "pictures":{},
                "subdirs":dirs,
                "display-recursive":"",
                "songs":{}}
        
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
    
class OldRoot:
    def index(self, directory = "."):
        html = """<html><body><h2>Here are the files in the selected directory:</h2>
        <a href="index?directory=%s">Up</a><br />
        """ % os.path.dirname(os.path.abspath(directory))

        for filename in glob.glob(directory + '/*'):
            absPath = os.path.abspath(filename)
            if os.path.isdir(absPath):
                html += '<a href="/index?directory=' + absPath + '">' + os.path.basename(filename) + "</a> <br />"
            else:
                html += '<a href="/download/?filepath=' + absPath + '">' + os.path.basename(filename) + "</a> <br />"
                
        html += """</body></html>"""
        return html
    index.exposed = True


if __name__ == '__main__':
    conf = {'global': {'tools.decode.encoding':"utf8", 'tools.encode.on':True, 'tools.decode.on':True, 'tools.encode.encoding':"utf8"}}
    root = Root()
    root.download = Download()
    cherrypy.quickstart(root, config = conf)
