""" grammar generator for gramcracker """

class GrammarWorker(object):
  micro = {}
  macro = {}
  digits = {} 
  specials = {}
  keygroups = {} 

  def __init__(self, sn):
    self.session = sn

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
    # go through each line looking for digits
    for x in line:
      if x.isdigit():
        value += x
      else:
        if value:
          bucket.append(value)
          value = ''
    # catch stragglers
    if value:
      bucket.append(value)

    for item in bucket:
      try:
        self.digits[item] += 1
      except KeyError:
        self.digits[item] = 1

  def parse_specials(self, line):
    """ parse a given line of special characters """
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
    """ parse micro format from a given line """
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

  def parse_macro(self, line):
    """ given a line parses macro definitions for that line """
    ret = ''
    char = ''
    for x in line:
      if x.isspace():
        continue
      elif x == char:
        continue
      else:
        ret += x
        char = x
    if ret != '':
      try:
        self.macro[ret] += 1
      except:
        self.macro[ret] = 1

  def parse(self, line):
    """
       Generate grammar tables for a given line
       This will populate the instance module
    """
    # population functions
    self.parse_specials(line)
    self.parse_digits(line)
    self.parse_micro(line)
    self.parse_macro(line)

