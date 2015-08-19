# lots of code used from other sites; not all my own work!
# Some code from http://stackoverflow.com/a/311634/2605023 and
# http://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/

# imports
import sys, os
import random
import struct, re
import numpy
import wave

if len(sys.argv) != 3:
    print 'Please provide the correct parameters: number of seconds and notes per second.'
    sys.exit(0)

FPS = 44100                                                                     # the original number of frames per second in a wave file

WAVSECONDS = int(sys.argv[1])                                                   # the number of seconds in the wav
NOTERATE   = int(sys.argv[2])                                                   # the number of notes per second
WAVLENGTH  = WAVSECONDS * FPS                                                   # the number of frames in the wav

CURRENTDIR = os.getcwd()                                                        # the current directory
WAVDIR     = CURRENTDIR + '/wavs/'                                              # the wav file directory
DIRFILES   = [filename for filename in os.listdir(WAVDIR) if os.path.isfile(WAVDIR + filename)] # filter for files only
WAVPATTERN = re.compile('^randomwav\d{3}.wav')
WAVFILES   = [file for file in DIRFILES if WAVPATTERN.match(file)]              # filter for wav files formatted as 'randomwav###.wav'
# WAVFILES.sort()                                                               # sort by number; not necessary right now
WAVFILECOUNT = len(WAVFILES)                                                    # number of existing wavs

FREQARRAY = [130.8, 138.6, 146.8, 155.6, 164.8, 174.6, 185.0,
             196.0, 207.7, 220.0, 233.1, 246.9, 261.6]                          # runs from C2 to C3 pitches

if WAVFILECOUNT > 1000:
    print 'Please clear your /wavs directory before continuing.'                # just for cleanliness
else:
    NewNumber = str(WAVFILECOUNT).zfill(3)                                      # next wav's index
    FileName  = WAVDIR + 'randomwav' + NewNumber + '.wav'                       # the wav's filename
    output = wave.open(FileName, 'w')                                           # create the wav
    output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))                # set the wav file's properties

    value_str = ''                                                              # this will contain the frames we write

    for i in range(0, WAVSECONDS * NOTERATE):                                   # for each note to be played
        value = FREQARRAY[random.randint(0, len(FREQARRAY) - 1)]                # pick a random one
        packed_value = struct.pack('h', value)                                  # write it to binary

        period = float(FPS / NOTERATE) / float(value)                           # calculate the period
        omega = numpy.pi * 2 / period                                           # and the omega
        xaxis = numpy.arange(int(period), dtype = numpy.float) * omega          # get the x-value
        ydata = 16384 * numpy.sin(xaxis)                                        # create a sin-wave

        signal = numpy.resize(ydata, (WAVLENGTH / NOTERATE,))                   # resize the sin-wave

        ssignal = ''                                                            # temporary holding value

        for j in range(len(signal)):                                            # write the sin-wave to a string
            ssignal += struct.pack('h', signal[j])
        value_str += ssignal                                                    # append the string to the total

    output.writeframes(value_str)                                               # write the frames to the wav
    output.close()                                                              # finished making wav

    if os.name == 'nt':                                                         # if on windows
        import winsound

        winsound.PlaySound(FileName, winsound.SND_FILENAME)                     # play using winsound
    elif os.name == 'posix':                                                    # if on OSX
        import subprocess

        subprocess.call(["afplay", FileName])                                   # call built-in afplay
    else:
        import ossaudiodev                                                      # else on UNIX

        s = wave.open(FileName, 'rb')                                           # play using ossaudio
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