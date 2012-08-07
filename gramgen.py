
if __name__ == '__main__':
    import argparse
    import sys, os, string, getopt, codecs
    import locale
    import subprocess

    from gramcracker import GrammarGenerator
    from gramcracker import Grammar
    reload(sys)
    sys.setdefaultencoding("utf_8")
    locale.setlocale(locale.LC_ALL,"")

    parser = argparse.ArgumentParser(
     description='This will create appropriate grammar files for cracking use')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--session',metavar='session_name',help='Session Name')
    args = parser.parse_args()
    g = GrammarGenerator(args.session)

    # send some passwords
    g.generate('foo124')
    g.generate('password')
    g.generate('foo1')
    g.generate('foo1392w82345')
    g.generate('foo1244')
    g.generate('1234')
    g.generate('1@#2!3**&(4')

    # parse the grammar
    grammar = Grammar(g)

    # define some verbosity
    if args.verbose:
        print grammar.grammar
        print grammar.digits
        print grammar.specials

    proc = subprocess.Popen(
                   ['/Users/rdriscoll/Downloads/john-1.7.9-jumbo-5-macosx-Intel-2/run/john',
                    '--stdin','--format=raw-sha1','/Users/rdriscoll/twitter/gits/pw_views/combo_not.txt',
                   ],
                   stdout=subprocess.PIPE,
                   stdin=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                    )
    i = 0
    while i == 0:
        output = proc.stdin.write('sex4rent')
        if output: i += 1
    


