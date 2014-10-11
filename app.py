#######################################################################
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#######################################################################
# WebSDR-Plus - A multi-user interface to an RTL-SDR
# (C) 2014 Iain R. Learmonth and contributors
#######################################################################
# For terms of redistribution and use see the LICENSE file.
#######################################################################

import numpy as np
from rtlsdr import RtlSdr
import time, threading
from flask import Flask, jsonify, render_template
from matplotlib.mlab import psd

NFFT = 1024 #*4
NUM_SAMPLES_PER_SCAN = NFFT*16

class Radio(object):

    def __init__(self, sdr):
        self.sdr = sdr

    def updateSamples(self):
        self.samples = self.sdr.read_samples(NUM_SAMPLES_PER_SCAN)
        self.psd_scan, self.f = psd(self.samples, NFFT=NFFT)
        threading.Timer(0.02, self.updateSamples).start()

    def getSamples(self):
        return self.psd_scan

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/2m.json")
def samples():
    return jsonify({'samples': radio.getSamples().tolist(), 'minf': 144.0e6, 'maxf': 146.0e6})

if __name__ == "__main__":
    sdr = RtlSdr()
    radio = Radio(sdr)

    # some defaults
    sdr.rs = 2.0e6
    sdr.fc = 145.0e6
    sdr.gain = 10

    # start polling for samples
    radio.updateSamples()

    app.run(debug=True, use_reloader=False, host='0.0.0.0')

