class Grammar(object):
    """
        Given a populated GrammarGenerator object a grammar table will be generated
    """

    def __init__(self,gens):
        self.grammar = {}
        self.digits = {}
        self.specials = {}
        def _calc_total(group):
            total = 0
            for value,count in group.iteritems():
                total += count
            return total

        def simplify(line):
            ret = ''
            char = ''
            for x in line:
                if x.isspace():
                    continue
                if x != char:
                    ret += x
                    char = x
            return ret

        def _groupings(group):
            # given a hash grouping of whatever combination
            # return an array of lengths in the keys
            keys = []
            for k in group.keys():
                try:
                    keys.index(len(str(k)))
                except:
                    keys.append(len(str(k)))
            return keys
            
        def _terminals(grp,length):
            total = 0
            for k in grp.keys():
                if len(str(k)) == length:
                    total += grp[k]
            return total

        self.macro = gens.macro
        macro_total = _calc_total(self.macro)
        for micro,count in gens.micro.iteritems():
            f1 = self.macro[simplify(micro)]
            f2 = float(f1) / macro_total
            f3 = float(count) / f1
            f4 = f2 * f3
            line = "%s%s%0.30f" %(micro,'\x09',f4)
            self.grammar[micro] = f4

        for x in _groupings(gens.digits):
            for k,v in gens.digits.iteritems():
                t =  _terminals(gens.digits,x)
                if len(str(k)) == x:
                    tmp_t = v
                    self.digits[k] = float(tmp_t)/t

        for x in _groupings(gens.specials):
            for k,v in gens.specials.iteritems():
                t =  _terminals(gens.specials,x)
                if len(str(k)) == x:
                    tmp_t = v
                    self.specials[str(k)] = float(tmp_t)/t
