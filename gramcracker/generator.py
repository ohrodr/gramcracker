""" grammar generator for gramcracker """
import unittest2

class GrammarTester(unittest2.TestCase):
  def test_gen_digits(self):
    g = GrammarGenerator('foo')
    g.parse_digits('1234')
    self.assertEqual(g.digits[str(1234)], 1)
    g.parse_digits("foo1234!4321")
    self.assertEqual(g.digits[str(1234)], 2)
    self.assertEqual(g.digits[str(4321)], 1)

  def test_gen_specials(self):
    g = GrammarGenerator('foo')
    g.parse_specials('$$$$!!!!')
    self.assertEqual(g.specials['$$$$!!!!'], 1)
    g.parse_specials('...afaf,,,')
    self.assertEqual(g.specials[',,,'], 1)
    self.assertEqual(g.specials['...'], 1)
    g.parse_specials('...foo,,,bar$$$$!!!!baz')
    self.assertEqual(g.specials[',,,'], 2)
    self.assertEqual(g.specials['...'], 2)
    self.assertEqual(g.specials['$$$$!!!!'], 2)

  def test_gen_micro(self):
    g = GrammarGenerator('foo')
    g.parse_micro('foo!1bar')
    self.assertEqual(g.micro['LLLSDLLL'], 1)
    g.parse_micro('bar1!foo')
    self.assertEqual(g.micro['LLLDSLLL'], 1)

  def test_parse(self):
    g = GrammarGenerator('foo')
    g.parse('foo1234!')
    self.assertEqual(g.digits[str(1234)], 1)
    self.assertEqual(g.specials['!'], 1)
    self.assertEqual(g.micro['LLLDDDDS'], 1)

class GrammarGenerator(object):

  def __init__(self, sn):
    self.micro = {}
    self.macro = {}
    self.digits = {} 
    self.specials = {}
    self.session = sn
    self.keygroups = {} 

  def parse_digits(self, line):
    """ given a line of input representing a password populate digits

        args:
          line -> string representing a password

        output:
           >>> g = generator.GrammarGenerator('foo')
           >>> g.digits
           {}
           >>> g._gen_digits('1234')
           >>> g.digits
           {'1': 4, '1234': 1, '123': 2, '12': 3}
    """
    bucket = []
    value = ''
    for x in line:
      if x.isdigit():
        value += x
      else:
        if value:
          bucket.append(value)
          value = ''
    if value:
      bucket.append(value)

    for item in bucket:
      try:
        self.digits[item] += 1
      except KeyError:
        self.digits[item] = 1

  def parse_specials(self, line):
    # < private function not to clutter module >
    # populate specials given a line input
    bucket = []
    val = ''
    for x in line:
      if x.isdigit() or x.isalpha():
        if val:
          bucket.append(val)
          val = ''
      else:
        val += x
    # this is for stragglers
    if val:
      bucket.append(val)

    for item in bucket:
      try:
        self.specials[item] += 1
      except KeyError:
        self.specials[item] = 1

  def parse_micro(self, line):
    # < private function not to clutter module >
    # let l be a place holder for character
    # that was last inspected
    # we do this to remove duplicates
    ret = u''
    for i in line:
      if i.isspace():
        continue
      elif i.isdigit():
        ret += "D"
      elif i.isalpha():
        ret += "L"
      else:
        ret += "S"

    try:
      self.micro[ret] += 1
    except:
      self.micro[ret] = 1
    return ret

  def parse(self, line):
    """
       Generate grammar tables for a given line
       This will populate the instance module
    """
    # population functions
    self.parse_specials(line)
    self.parse_digits(line)
    self.parse_micro(line)