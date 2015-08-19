# imports
import sys, os
import random
import struct, re
import numpy
import wave

if len(sys.argv) != 4:
    print 'Please provide the correct parameters: wav file to read, number of seconds, number of notes per second.'
    sys.exit(0)

read = wave.open(sys.argv[1], 'r')                          # open the wav file to be played
(nchannels, sampwidth, framerate, nframes, _, _) = read.getparams () # get metadata of the wav file
frames = read.readframes(nchannels * nframes)               # read all the frames in the wave file
framelist = struct.unpack_from("%dh" % nframes * nchannels, frames)     # unpack all the frames
freqarray = set()                                           # array to store frequencies

for frame in framelist:                                     # add all of the frames
    freqarray.add(frame)

FPS = 44100

WAVSECONDS = int(sys.argv[2])                                                   # the number of seconds in the wav
NOTERATE   = int(sys.argv[3])                                                   # the number of notes per second
WAVLENGTH  = WAVSECONDS * FPS                                                   # the number of frames in the wav

CURRENTDIR = os.getcwd()                                                        # the current directory
WAVDIR     = CURRENTDIR + '/wavs/'                                              # the wav file directory
DIRFILES   = [filename for filename in os.listdir(WAVDIR) if os.path.isfile(WAVDIR + filename)] # filter for files only
WAVPATTERN = re.compile('^randomwav\d{3}.wav')
WAVFILES   = [file for file in DIRFILES if WAVPATTERN.match(file)]              # filter for wav files formatted as 'randomwav###.wav'
# WAVFILES.sort()                                                               # sort by number; not necessary right now
WAVFILECOUNT = len(WAVFILES)                                                    # number of existing wavs

if WAVFILECOUNT > 1000:
    print 'Please clear your /wavs directory before continuing.'                # just for cleanliness
else:
    NewNumber = str(WAVFILECOUNT).zfill(3)                                      # next wav's index
    FileName  = WAVDIR + 'randomwav' + NewNumber + '.wav'                       # the wav's filename
    output = wave.open(FileName, 'w')                                           # create the wav
    output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))                # set the wav file's properties

    value_str = ''                                                              # this will contain the frames we write

    for i in range(0, WAVSECONDS * NOTERATE):                                   # for each note to be played
        value = abs(random.sample(freqarray, 1)[0] / 16384.0 * 880.0)           # pick a random value and convert to audible freq
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