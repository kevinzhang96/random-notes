# random-notes
Python script to generate musical notes.  Used for music training (matching pitches)

# Usage
To generate a random sound file:
From command line, cd into the directory and do 'python generate.py 3 4', where 3 is the number of seconds you want it to last and 4 is the number of notes per second.  The pitches used right now are C2 through C3.

To generate a random sound file from a .wav file:
From command line, cd into the directory and do 'python readplay.py filename.wav 3 4', where filename.wav is the file you want to use as the seed, 3 is the number of seconds you want it to last and 4 is the number of notes per second.  The pitches in the wav file given are converted to the standard pitch range (0 to 880) and played.
