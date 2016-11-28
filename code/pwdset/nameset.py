# 用来处理姓名

class CnameSet(object):
    """姓名拼音处理，返回字段和优先级"""
    def __init__(self, arg):
        super(CnameSet, self).__init__()
        self.all = []
        self.set_all(arg)
    def set_all(self, s):
        # 如果是str直接处理
        if s and isinstance(s, str):
            pieces        = s.lower().split(' ')
            nm_long       = (1, ''.join(pieces))
            nm_short      = (1, ''.join(x[0] for x in pieces))
            nm_last       = (1, pieces[0])
            nm_short_up   = (2, nm_short[1].upper())
            nm_last_title = (2, pieces[0].title())
            self.all      += [nm_long, nm_short, nm_last, nm_short_up, nm_last_title]
        # 如果是list则循环处理
        elif isinstance(s, list):
            for x in s:
                self.set_all(x)

class EnameSet(object):
    """英文名处理，返回字段和优先级"""
    def __init__(self, arg):
        super(EnameSet, self).__init__()
        self.all = []
        self.set_all(arg)
    def set_all(self, s):
        # 如果是str直接处理
        if s and isinstance(s, str):
            pieces         = s.lower().split(' ')
            nm_first       = (2, pieces[0])
            nm_first_title = (3, pieces[0].title())
            self.all       += [nm_first, nm_first_title]
            if len(pieces) > 1:
                nm_last        = (2, pieces[1])
                nm_last_title  = (3, pieces[1].title())
                self.all = [nm_last, nm_last_title]
        # 如果是list则循环处理
        elif isinstance(s, list):
            for x in s:
                self.set_all(x)
        

# if __name__ == '__main__':
#     c = CnameSet(['Wang da chui', 'zhang wei'])
#     e = EnameSet(['Jack Ma', 'tom ding'])
#     print(c.all)
#     print(e.all)