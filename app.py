#######################################################################
# WebSDR-Plus - A multi-user interface to an RTL-SDR
# (C) 2014 Iain R. Learmonth and contributors
#######################################################################
# For terms of redistribution and use see the LICENSE file.
#######################################################################
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#######################################################################

import numpy as np
from rtlsdr import RtlSdr
import time, threading
from flask import Flask, jsonify

NFFT = 1024*4
NUM_SAMPLES_PER_SCAN = NFFT*16

class Radio(object):

    def __init__(self, sdr):
        self.sdr = sdr

    def updateSamples(self):
        self.samples = self.sdr.read_samples(NUM_SAMPLES_PER_SCAN)
        threading.Timer(0.2, self.updateSamples).start()

    def getSamples(self):
        return [np.absolute(x).tolist() for x in self.samples.tolist()]

app = Flask(__name__)

@app.route("/")
def hello():
    return "WebSDR-Plus!"

@app.route("/2m.json")
def hello():
    return jsonify({'samples': radio.getSamples(), 'minf': 144.0e6, 'maxf': 146.0e6})

if __name__ == "__main__":
    sdr = RtlSdr()
    radio = Radio(sdr)

    # some defaults
    sdr.rs = 2.0e6
    sdr.fc = 145.0e6
    sdr.gain = 10

    # start polling for samples
    radio.updateSamples()

    app.run()

