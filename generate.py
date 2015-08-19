import os
import re
import wave

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
    