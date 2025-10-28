from flask import Flask
from flask import request
import os
import threading
import time

 #Since it runs in sperate threads . user should take care of killing the app running . so only we have shutdown feature to stop. else wont able to kill
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    print("hello world")
    return 'Hello World'


@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    print("Shutting down Flask server...")
    threading.Thread(target=_delayed_exit, daemon=False).start()
    return 'Server shutting down...'

def _delayed_exit():
    time.sleep(0.5)
    os._exit(0)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False,use_reloader=False)
