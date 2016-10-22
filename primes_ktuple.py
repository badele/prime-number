#!/usr/bin/env python

import lib
import sys

import prettyplotlib as ppl
import numpy as np

import matplotlib.pyplot as plt

if __name__=='__main__':

    # Parse command line options
    if len(sys.argv)<=1:
        print "Please set loop numbers"
        sys.exit()

    graph=False
    if len(sys.argv)>2:
        graph=True

    # Vars
    n = int(sys.argv[1])
    div = 100
    step = n / div

    # Compute primes
    primes = lib.primesfrom3to(n)
    ktuples = np.subtract(np.roll(primes, -1), primes)[:-1]
    x = np.linspace(1,len(ktuples)+1,num=len(ktuples)+1)
    uktuples,uidx, ridx, cktuples = np.unique(ktuples,return_index=True,return_inverse=True, return_counts=True)
    maxcktuples = np.max(cktuples)

    loopnumber = lib.human_format(n)
    print "First max k-tuples apparition for %(loopnumber)s" % locals()
    lastprime = 1
    for idx in uidx:
        reverseidx = ridx[idx]
        firstprime = primes[idx]
        secondprime = primes[idx+1]
        ktuple = uktuples[reverseidx]
        count = cktuples[reverseidx]

        before=''
        if firstprime<lastprime:
            before = ' appear before previous lines'

        ismax=''
        if count==maxcktuples:
            ismax = ' (MAX)'

        print "%(firstprime)s %(secondprime)s => %(ktuple)s x %(count)s%(ismax)s%(before)s" % locals()
        lastprime = secondprime


    # Graph
    if not graph:
        sys.exit()

    fig, ax = ppl.subplots(1)
    plt.ylabel('First k-tuples apparition')
    plt.xlabel('# prime numbers')

    ppl.plot(uidx+1,uktuples,'-')
    ppl.plot(uidx+1,uktuples,'o')

    # Change y axis
    plt.ylim(ymin=0)

    # Change x axis label
    if n>10:
        ax.get_xaxis().get_major_formatter().set_scientific(False)
        fig.canvas.draw()
        labels = [lib.human_format(int(item.get_text())) for item in ax.get_xticklabels()]
        ax.set_xticklabels(labels)
        ax = plt.gca()

    ppl.legend(ax,loc='lower right',)
    plt.grid()
    plt.show()
