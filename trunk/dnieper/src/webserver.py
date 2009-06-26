import glob
import os.path
import sys
import StringIO
import cherrypy

from cherrypy.lib.static import serve_file, serve_fileobj
from ezt import Template
from Entities import Entity, FileInfo
from tempfile import NamedTemporaryFile

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
    
    
    def make_playlist(self, urlList):
        f = StringIO.StringIO()
        
        for url in urlList:
            f.write(url + "\n")
        
        return f
    
    def index(self, filepath):
        mime = "application/x-download"
        
        if filepath.endswith(".m3u"):
            server = "http://%s:%s" % (cherrypy.request.app.config['global']['server.socket_host'], cherrypy.request.app.config['global']['server.socket_port'])

            f = self.make_playlist([server + "/root/download/?filepath=" + filepath])
            
            print f.getvalue()
            
            return serve_fileobj(f, "audio/x-mpegurl", "attachment")
        elif filepath.endswith(".m3u"):
            mime = "audio/mpeg"
        
        return serve_file(filepath, mime, "attachment")
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
