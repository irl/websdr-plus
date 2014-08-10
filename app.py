#######################################################################
# WebSDR-Plus - A multi-user interface to an RTL-SDR
# (C) 2014 Iain R. Learmonth and contributors
#######################################################################
# For terms of redistribution and use see the LICENSE file.
#######################################################################
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#######################################################################

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
        return "WebSDR-Plus!"

if __name__ == "__main__":
        app.run()

