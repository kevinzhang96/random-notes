# completed using http://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/ as a reference

import sys
import os
import struct
import re
import wave

if sys.argv.count() != 1:
    print 'Please provide the correct parameters: number of seconds.'
    sys.exit(0)

WAVLENGTH = int(sys.argv[0])
# NOTERATE  = int(sys.argv[1])

CURRENTDIR = os.getcwd()
WAVEDIR    = CURRENTDIR + '/wavs/'
DIRFILES   = [filename for filename in os.listdir(WAVEDIR) if os.path.isfile(WAVEDIR + filename)]
WAVPATTERN = re.compile('^randomwav\d{3}.wav')
WAVFILES   = [file for file in DIRFILES if WAVPATTERN.match(file)]
WAVFILES.sort()
WAVFILECOUNT = WAVFILES.count()

if WAVFILECOUNT > 1000:
    print 'Please clear your /wavs directory before continuing; too many random files have been generated.'
else:
    NewNumber = str(WAVFILECOUNT).zfill(3)
    FileName  = 'randomwav' + NewNumber + '.wav'
    output = wave.open(FileName, 'w')
    output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

    values = []

    for i in range(0, WAVLENGTH):
        value = random.randint(-32767, 32767)
        packed_value = struct.pack('h', value)
        values.append(packed_value)
        values.append(packed_value)

    value_str = ''.join(values)
    output.writeframes(value_str)
    output.close()