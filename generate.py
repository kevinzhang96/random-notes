# completed using http://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/ as a reference

import sys
import os
import random
import struct
import numpy
import re
import wave

if len(sys.argv) != 3:
    print 'Please provide the correct parameters: number of seconds and notes per second.'
    sys.exit(0)

FPS = 44100 # the original number of frames per second in a wave file

WAVSECONDS = int(sys.argv[1])
WAVLENGTH  = WAVSECONDS * FPS
NOTERATE   = int(sys.argv[2])

CURRENTDIR = os.getcwd()
WAVDIR    = CURRENTDIR + '/wavs/'
DIRFILES   = [filename for filename in os.listdir(WAVDIR) if os.path.isfile(WAVDIR + filename)]
WAVPATTERN = re.compile('^randomwav\d{3}.wav')
WAVFILES   = [file for file in DIRFILES if WAVPATTERN.match(file)]
WAVFILES.sort()
WAVFILECOUNT = len(WAVFILES)

FREQARRAY = [130.8, 138.6, 146.8, 155.6, 164.8, 174.6, 185.0, 196.0, 207.7, 220.0, 233.1, 246.9, 261.6]

if WAVFILECOUNT > 1000:
    print 'Please clear your /wavs directory before continuing; too many random files have been generated.'
else:
    NewNumber = str(WAVFILECOUNT).zfill(3)
    FileName  = WAVDIR + 'randomwav' + NewNumber + '.wav'
    output = wave.open(FileName, 'w')
    output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

    value_str = ''

    for i in range(0, WAVSECONDS * NOTERATE):
        value = FREQARRAY[random.randint(0, len(FREQARRAY) - 1)]
        packed_value = struct.pack('h', value)

        period = float(FPS / NOTERATE) / float(value)
        omega = numpy.pi * 2 / period
        xaxis = numpy.arange(int(period), dtype = numpy.float) * omega
        ydata = 16384 * numpy.sin(xaxis)

        signal = numpy.resize(ydata, (WAVLENGTH / NOTERATE,))

        ssignal = ''

        for j in range(len(signal)):
            ssignal += struct.pack('h', signal[j])
        value_str += ssignal

    output.writeframes(value_str)
    output.close()

    if os.name == 'nt':
        import winsound

        winsound.PlaySound(FileName, winsound.SND_FILENAME)
    elif os.name == 'posix':
        import subprocess

        subprocess.call(["afplay", FileName])
    else:
        import ossaudiodev

        s = wave.open(FileName, 'rb')
        (nc, sw, fr, nf, comptype, compname) = s.getparams()
        dsp = ossaudiodev.open('/dev/dsp', 'w')
        try:
            from ossaudiodev import AFMT_S16_NE
        except ImportError:
            if byteorder == 'little':
                AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
            else:
                AFMT_S16_NE = ossaudiodev.AFMT_S16_BE
        dsp.setparameters(AFMT_S16_NE, nc, fr)
        data = s.readframes(nf)
        s.close()
        dsp.write(data)
        dsp.close()