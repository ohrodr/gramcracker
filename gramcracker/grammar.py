from collections import defaultdict

class GrammarManager(object):
  """
      Given a populated GrammarWorker object a grammar table will be generated

      This module class creates a "probability table" for grammars you should generate passwords for.
      This greatly decreases the keyspace over time.  The manager also keeps track of each
      grammar worker result used to build the table.  This can be useful for deduplication.

  """

  def __init__(self,worker=None):
    self.grammar = {}
    self.digits = {}
    self.specials = {}
    if worker:
      self.current_worker = worker
    else:
      self.current_worker = None
    self.worker_log = defaultdict(list)

  def _calc_total(self, group):
    """ calculate totals for a given group """
    total = 0
    for value, count in group.iteritems():
      total += count
    return total

  def simplify(self, line):
    """ simplify by removing duplicate entries """
    ret = ''
    char = ''
    for x in line:
      if x.isspace():
        continue
      if x != char:
        ret += x
        char = x
    return ret

  def _groupings(self, group):
    """ given a group return an array of lengths of keys """
    keys = []
    for k in group.keys():
      try:
        keys.index(len(str(k)))
      except:
        keys.append(len(str(k)))
    return keys
          
  def _terminals(self, grp,length):
    """ total groups by length """
    total = 0
    for k in grp:
      if len(str(k)) == length:
        total += grp[k]
    return total

  def new_worker(self, worker):
    """ this sets a new worker for the instance given GrammarWorker """
    if self.current_worker:
      self.worker_log[self.current_worker.session].append(self.current_worker)
    self.current_worker = worker

  def _calculate_group(self, result_dict, store_here):
    """ given a result dict and attr string does math on grammarworker """
    for x in self._groupings(result_dict):
      for k, v in result_dict.iteritems():
        t = self._terminals(result_dict, x)
        if len(str(k)) == x:
          tmp_t = v
          value_attr = getattr(self, store_here)
          if k not in value_attr:
            value_attr[k] = float(tmp_t) / t
          else:
            value_attr[k] = float(tmp_t) / t
          setattr(self, store_here, value_attr)

  def calculate(self):
    """ this does the actual calculation of the current worker """
    if not self.current_worker:
      raise AttributeError("Please add a new_worker")

    macro_total = self._calc_total(self.current_worker.macro)
    for micro,count in self.current_worker.micro.iteritems():
      macro = self.current_worker.macro
      try:
        f1 = macro[self.simplify(micro)]
      except KeyError:
        macro[self.simplify(micro)] = 1
        f1 = macro[self.simplify(micro)]
      f2 = float(f1) / macro_total
      f3 = float(count) / f1
      f4 = f2 * f3
      line = "%s%s%0.30f" %(micro,'\x09',f4)
      self.grammar[micro] = f4
    
    self._calculate_group(self.current_worker.digits, 'digits')
    self._calculate_group(self.current_worker.specials, 'specials')