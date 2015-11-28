#!/usr/bin/python2.7
""" This script leverages dynamodb pipeline export data to calculate and generate a basic graph.  The idea is to help visualize how this utility library is useful.
"""
__author__ = "rodr <rodr@dpustudios.com>"
import argparse
import json
import locale
import os
import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 

from gramcracker import GrammarWorker
from gramcracker import GrammarManager

if __name__ == '__main__':
  reload(sys)
  sys.setdefaultencoding("utf_8")
  locale.setlocale(locale.LC_ALL, "")

  parser = argparse.ArgumentParser(
    description='This will create appropriate grammar files for cracking use')
  parser.add_argument('--verbose', '-v', action='count')
  parser.add_argument('--session',
    metavar='session_name',
    default='gramcracker',
    help='Session Name',)
  parser.add_argument('--filename', '-f', metavar='pwlist', help='file of listed passwords')
  args = parser.parse_args()
  g = GrammarWorker(args.session)

  # send some passwords
  if not os.path.isfile(args.filename):
    print "Please provide a valid password file."
    sys.exit(1)

  with open(args.filename) as fh:
    for line in fh.readlines():
      json_dict = json.loads(line)
      g.parse(json_dict["cookie_value"]["s"])
  # parse the grammar
  grammar = GrammarManager(worker=g)
  grammar.calculate()
  # define some verbosity
  if args.verbose:
    print grammar.grammar
    print grammar.digits
    #print grammar.specials
    hg = grammar.digits.values()
    hg.sort()
    hgmean = np.mean(hg)
    hgstd = np.std(hg)
    hgpdf = stats.norm.pdf(hg, hgmean, hgstd)
    plt.plot(hg, hgpdf)
    plt.savefig('myfig')
