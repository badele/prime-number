#!/usr/bin/env python

import lib
import timeit
import sys
import math
import datetime

import prettyplotlib as ppl
import numpy as np

import matplotlib.pyplot as plt
from prettyplotlib import brewer2mpl

primenumbers_gen = [
    'sieveOfEratosthenes',
    'ambi_sieve',
    'ambi_sieve_plain',
    'sundaram3',
    'sieve_wheel_30',
    'primesfrom3to',
    'primesfrom2to',
    'rwh_primes',
    'rwh_primes1',
    'rwh_primes2',
]

if __name__=='__main__':

    # Vars
    n = 10000000 # number itereration generator
    nbcol = 5 # For decompose prime number generator
    nb_benchloop = 3 # Eliminate false positive value during the test (bench average time)
    datetimeformat = '%Y-%m-%d %H:%M:%S.%f'
    config = 'from __main__ import n; import lib'
    primenumbers_gen = {
        'sieveOfEratosthenes': {'color': 'b'},
        'ambi_sieve': {'color': 'b'},
        'ambi_sieve_plain': {'color': 'b'},
         'sundaram3': {'color': 'b'},
        'sieve_wheel_30': {'color': 'b'},
# # #        'primesfrom2to': {'color': 'b'},
        'primesfrom3to': {'color': 'b'},
        # 'rwh_primes': {'color': 'b'},
        # 'rwh_primes1': {'color': 'b'},
        'rwh_primes2': {'color': 'b'},
    }


    # Get n in command line
    if len(sys.argv)>1:
        n = int(sys.argv[1])

    step = int(math.ceil(n / float(nbcol)))
    nbs = np.array([i * step for i in range(1, int(nbcol) + 1)])
    set2 = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors

    print datetime.datetime.now().strftime(datetimeformat)
    print("Compute prime number to %(n)s" % locals())
    print("")

    results = dict()
    for pgen in primenumbers_gen:
        results[pgen] = dict()
        benchtimes = list()
        for n in nbs:
            t = timeit.Timer("lib.%(pgen)s(n)" % locals(), setup=config)
            execute_times = t.repeat(repeat=nb_benchloop,number=1)
            benchtime = np.mean(execute_times)
            benchtimes.append(benchtime)
        results[pgen] = {'benchtimes':np.array(benchtimes)}

fig, ax = plt.subplots(1)
plt.ylabel('Computation time (in second)')
plt.xlabel('Numbers computed')
i = 0
for pgen in primenumbers_gen:

    bench = results[pgen]['benchtimes']
    avgs = np.divide(bench,nbs)
    avg = np.average(bench, weights=nbs)

    # Compute linear regression
    A = np.vstack([nbs, np.ones(len(nbs))]).T
    a, b = np.linalg.lstsq(A, nbs*avgs)[0]

    # Plot
    i += 1
    #label="%(pgen)s" % locals()
    #ppl.plot(nbs, nbs*avgs, label=label, lw=1, linestyle='--', color=set2[i % 12])
    label="%(pgen)s avg" % locals()
    ppl.plot(nbs, a * nbs + b, label=label, lw=2, color=set2[i % 12])
print datetime.datetime.now().strftime(datetimeformat)

ppl.legend(ax, loc='upper left', ncol=4)

# Change x axis label
ax.get_xaxis().get_major_formatter().set_scientific(False)
fig.canvas.draw()
labels = [lib.human_format(int(item.get_text())) for item in ax.get_xticklabels()]
ax.set_xticklabels(labels)
ax = plt.gca()

plt.grid()
plt.show()
