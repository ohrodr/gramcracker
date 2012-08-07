class GrammarGenerator(object):
    def __init__(self,sn):
        self.micro = {}
        self.macro = {}
        self.digits = {} 
        self.specials = {}
        self.session = sn
        self.keygroups = {} 

    def __repr__(self):
        return repr(self.session)

    def generate(self,line):
        """
           Generate grammar tables for a given line
           This will populate the instance module
        """

        # private function definitions

        def _gen_digits(self,line):
            # < private function not to clutter module >
            # populate digits given a line input
            bucket = []
            value = ''
            for x in line:
                if x.isdigit():
                    value += x
                else:
                    if value:
                        bucket.append(value)
                        value = ''
            if x.isdigit():
                bucket.append(value)
            for item in bucket:
                try:
                    self.digits[item] += 1
                except: 
                    self.digits[item] = 1
                

        def _gen_specials(line):
            # < private function not to clutter module >
            # populate specials given a line input
            bucket = []
            val = ''
            for x in line:
                if x.isdigit():
                    if val:
                        bucket.append(val)
                        val = ''
                elif x.isalpha():
                    if val:
                        bucket.append(val)
                        val = ''
                else:
                    val += x
            if val:
                bucket.append(val)
            for item in bucket:
                try:
                    self.specials[item] += 1
                except:
                    self.specials[item] = 1
    

        def _gen_micro(line):
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

        def _gen_keygroups(self,grp,grp_key):
            try:
                self.keygroups[grp_key]
            except:
                self.keygroups[grp_key] = {}

            for k in grp:
                str_len = len(str(k))
                if self.keygroups[grp_key].get(str_len):
                    self.keygroups[grp_key][str_len] += 1
                else:
                    self.keygroups[grp_key][str_len] = 1

        # population functions
        _gen_specials(line)
        _gen_digits(self,line)
        _gen_keygroups(self,self.digits,'digits')
        ret = u''
        char = u''
        n = _gen_micro(line)
        for x in n:
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

