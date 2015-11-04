import unittest2

from generator import GrammarWorker
from grammar import GrammarManager

class GrammarManagerTester(unittest2.TestCase):
  def test_create(self):
    g = GrammarWorker("foo")
    g.parse("foo1234")
    gr = GrammarManager(worker=g)
    gr.calculate()
    self.assertEqual(gr.grammar["LLLDDDD"], 1.0)
  
  def test_append_grammar(self):  
    g = GrammarWorker("foo")
    g.parse("foo1234")
    gr = GrammarManager(worker=g)
    gr.calculate()

    g.parse("foo")
    gr.new_worker(g)
    gr.calculate()
    self.assertEqual(gr.grammar["LLLDDDD"], 0.3333333333333333)
    self.assertEqual(gr.grammar["LLL"], 0.3333333333333333)
    self.assertEqual(len(gr.grammar), 2)

    g.parse('bazbiff')
    gr.new_worker(g)
    gr.calculate()
    self.assertEqual(gr.grammar["LLLLLLL"], 0.2)
    self.assertFalse(gr.grammar["LLL"] == 0.3)
    self.assertEqual(len(gr.grammar), 3)
  
  def test_log(self):
    g = GrammarWorker("foo")
    g.parse("foo1234")
    gr = GrammarManager(worker=g)
    gr.calculate()
    self.assertEqual(len(gr.worker_log), 0)
    g.parse("foo")
    gr.new_worker(g)
    self.assertEqual(len(gr.worker_log), 1)
    self.assertTrue('foo' in gr.worker_log)
    self.assertTrue(gr.worker_log['foo'][0].micro['LLL'] == 1)
    
  def test_calculate_without_worker(self):
    gr = GrammarManager()
    with self.assertRaises(AttributeError):
      gr.calculate()

  def test_digits(self):
    g = GrammarWorker("foo")
    gr = GrammarManager()
    g.parse("foo1234")
    gr.new_worker(g)
    gr.calculate()
    self.assertEqual(gr.digits['1234'], 1.0)
    g.parse("foo1234!4321")
    gr.new_worker(g)
    gr.calculate()
    self.assertEqual(gr.digits['4321'], 0.3333333333333333)
    self.assertTrue(gr.digits['1234'] < 1.0)