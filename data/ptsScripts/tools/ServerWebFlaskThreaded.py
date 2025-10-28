from flask import Flask
import threading
from werkzeug.serving import make_server
import kTools; tls = kTools.KTools()

 #Since it runs in sperate threads . user should take care of killing the app running . so only we have shutdown feature to stop. else wont able to kill
 
# Flask constructor takes the name of 
# current module (__name__) as argument.

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)        
        self.server = make_server('127.0.0.1', 5000, app)
        print("Staring server http://{}:{}".format(self.server.host, self.server.port))
        print("Use http://{}:{}/shutdown to stop the server".format(self.server.host, self.server.port))
        self.ctx = app.app_context()
        self.ctx.push()
        self.daemon = True

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

app = Flask(__name__)
server = ServerThread(app)
    
@app.route('/')
def hello():
    return "Hello from server! - " + str(tls.getTimeStamp())

@app.route('/send')
def action1():
    PTS.MainQueue.put({ "action" : "exec_script" , "params" :  {"scriptFile" : r'G:\pyworkspace\PyTasky\data\ptsScripts\tools\cryptprice.py' } })
    return "main-send!"	

@app.route('/send2')
def action2():
    PTS.MainQueue.put({ "action" : "exec_script" , "params" :  {"scriptFile" : r'G:\pyworkspace\PyTasky\data\ptsScripts\poc\xmlpather.py' } })
    return "send2!"    
	
@app.route('/shutdown')
def shutdown():
    print("Server shutting down... Bye!")
    threading.Thread(target=server.stop).start()
    return "Server shutting down... Bye!"

if __name__ == '__main__':
    server.start()
