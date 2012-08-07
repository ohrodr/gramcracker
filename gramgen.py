
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
    parser.add_argument('--filename','-f',metavar='pwlist',help='file of listed passwords')
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

