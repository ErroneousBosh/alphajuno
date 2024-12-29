#!/usr/bin/python

import numpy as np
import scipy.io.wavfile as wav
import scipy.fftpack
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

s_len = 640       # how many samples to generate

pwval = 42	  # PWM width

# blank array to hold the samples
s_a = np.zeros(s_len)


for i in range(0, s_len):
    
    # saw counter goes from 0 to 255
    saw = i & 0xff

    # a note about the code idiom you see below
    # the [0x00, 0xff] bit is the low and high output value
    # sent to the output, as a list
    # the expression after it is either True or False which
    # becomes 1 or 0, selecting the appropriate value in the list
    
    # square is high if the high bit of the saw counter is
    sqr = [0x00,0xff][saw & 0x80 != 0]
    # square one octave up, from bit 6 of the saw counter
    oct1 = [0x00,0xff][saw & 0x40 != 0]
    # square three octave up, from bit 4 of the saw counter
    oct3 = [0x00,0xff][saw & 0x10 != 0]
    # pw gates the square and saw output, from 0 to 127
    pw = [0x00,0xff][(saw & 0x7f) >= pwval]

    # note that the PW being 0 to 127 is further evidence that the 
    # saw counter is 8-bit, I think
    # if 127 is a tiny thin pulse it must be "greater than or equal"

    # output expressions
    # uncomment one to select the output
    # square 1, just square
    #out = sqr

    # square 2, 25% PW fixed
    #out = sqr & oct1

    # square 3, PWM
    #out = sqr & pw

    # saw 1, just saw
    #out = saw

    # saw 2, saw chopped at octave
    #out = saw & oct1

    # saw 3, saw PWM
    #out = saw & pw

    # saw 4, saw chopped at 3 octaves
    #out = saw & oct3

    # saw 5, saw chopped at both
    out = saw & oct1 & oct3

    s_a[i] = out

# output the actual plot
plt.style.use('dark_background')	# sillyscope colours
fig = plt.figure(figsize=(6,2.2))	# similar size to aciddose's
plt.title('Saw 05')
plt.plot(s_a, linewidth=2)		# fatten up the line when we plot
plt.xticks(range(0, s_len + 1, 64))	# ticks in 64-clock steps
#plt.savefig('saw05.jpg')		# uncomment to save the image
plt.show()				# comment to save without showing
