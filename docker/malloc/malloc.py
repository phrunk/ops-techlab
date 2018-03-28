#!/usr/bin/env python

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    global buffer

    try:
        mem = float(path)
    except:
        mem = None
    #mem = request.args.get('mem', type=int)
    if mem >= 0:
        mem = int(mem * 1024 ** 2)
        buffer = bytearray(mem)

        return "Resized buffer to " + str(len(buffer)) + " bytes\n"
    else:
        return "Please specify memory to allocate in megabytes, e.g.: " + request.host_url + "1000\n"


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, threaded=True)
