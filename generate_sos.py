#!/usr/bin/env python3
"""Generates a waveform that gets loaded into the Juntek JDS2800 Signal Generator. The waveform
contains a SOS in Morse code."""

from jds6600 import jds6600

SG_SERIAL_PORT = "/dev/ttyUSB0"
WF_SLOT = 1  # Arbitrary waveform # to write to

# Lengths of the dots and dashes in the morse code
BASE_LENGTH = 12
DAH_LENGTH = 20
DIT_LENGTH = 8
SPACE_LENGTH = 5

LINE_VALUE = 4095  # Max value that can go in the waveform array
WF_LEN = 2048  # Max number of values that can go in the waveform array

# array we'll populate and then write to the signal generator
wf = [0] * WF_LEN
pos = 0

# Used to disable writing to the device while debugging
WRITE_TO_SG = False
WRITE_TO_SG = True


def space():
    global pos
    for ii in range(SPACE_LENGTH * BASE_LENGTH):
        wf[pos] = 0
        pos += 1


def dit():
    global pos
    for ii in range(DIT_LENGTH * BASE_LENGTH):
        wf[pos] = LINE_VALUE
        pos += 1
    space()


def dah():
    global pos
    for ii in range(DAH_LENGTH * BASE_LENGTH):
        wf[pos] = LINE_VALUE
        pos += 1
    space()


def S():
    dit()
    dit()
    dit()


def O():
    dah()
    dah()
    dah()


if __name__ == "__main__":
    S()
    O()
    S()

    print(f"Wrote {pos} values to the array")
    print(f"Length of wf = {len(wf)}")
    if WRITE_TO_SG:
        sg = jds6600(SG_SERIAL_PORT)
        sg.arb_setwave(WF_SLOT, wf)
        print("Wrote waveform to signal generator")
