import argparse
import json
import locale
import os
import sys

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
    print grammar.specials
