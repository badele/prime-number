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

    # Compute primes
    primes = lib.primesfrom3to(n)
    for p in primes:
        p = long(p)
        r = lib.calc_mersenne(p)
        if not lib.is_probable_prime(r):
            print "M%(p)s is not mersenne prime" % locals()


