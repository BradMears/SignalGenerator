#!/usr/bin/env python3
"""Generates a waveform that gets loaded into the Juntek JDS2800 Signal Generator. The waveform
contains a mathematical function of no significance except it looks distinctive compared to the
built-in waveforms."""

from math import sin, pi
from jds6600 import jds6600

SG_SERIAL_PORT = "/dev/ttyUSB0"
WF_SLOT = 2  # Arbitrary waveform # to write to

LINE_VALUE = 4095  # Max value that can go in the waveform array
WF_LEN = 2048  # Max number of values that can go in the waveform array

# Used to disable writing to the device while debugging
WRITE_TO_SG = False
WRITE_TO_SG = True


if __name__ == "__main__":

    # array we'll populate and then write to the signal generator
    wf = [0] * WF_LEN

    # Temporary array we use for floating point calculations until we convert to integer
    twf = [0] * WF_LEN

    # To get a smooth curve, use a step size of 2 pi radians divided by the maximum number
    # of entries in the waveform
    step_size = 2 * pi / WF_LEN
    for ii in range(WF_LEN):
        x = step_size * ii
        val = (
            sin(x) + sin(2 * x) + sin(3 * x)
        )  # No significance to this equation. Use any you like
        twf[ii] = val

    # Normalize and scale to 0 - LINE_VALUE
    min_value = min(twf)
    for ii in range(WF_LEN):
        twf[ii] = twf[ii] - min_value
    max_value = max(twf)
    scale = LINE_VALUE // max_value
    for ii in range(WF_LEN):
        wf[ii] = round(twf[ii] * scale)

    if WRITE_TO_SG:
        sg = jds6600(SG_SERIAL_PORT)
        sg.arb_setwave(WF_SLOT, wf)
        print("Wrote waveform to signal generator")
    print("Finished")
