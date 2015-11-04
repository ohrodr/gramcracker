
import unittest2

from generator import GrammarWorker

class GrammarWorkerTester(unittest2.TestCase):
  def test_gen_digits(self):
    g = GrammarWorker('foo')
    g.parse_digits('1234')
    self.assertEqual(g.digits[str(1234)], 1)
    g.parse_digits("foo1234!4321")
    self.assertEqual(g.digits[str(1234)], 2)
    self.assertEqual(g.digits[str(4321)], 1)

  def test_gen_specials(self):
    g = GrammarWorker('foo')
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
    g = GrammarWorker('foo')
    g.parse_micro('foo!1bar')
    self.assertEqual(g.micro['LLLSDLLL'], 1)
    g.parse_micro('bar1!foo')
    self.assertEqual(g.micro['LLLDSLLL'], 1)

  def test_gen_macro(self):
    g = GrammarWorker('foo')
    g.parse_macro("foo12344")
    self.assertEqual(g.macro['fo1234'], 1)

  def test_parse(self):
    g = GrammarWorker('foo')
    g.parse('foo1234!')
    self.assertEqual(g.digits[str(1234)], 1)
    self.assertEqual(g.specials['!'], 1)
    self.assertEqual(g.micro['LLLDDDDS'], 1)
