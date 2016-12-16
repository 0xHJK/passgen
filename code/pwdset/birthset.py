# 用来处理生日

class BirthSet(object):
    """用来处理生日，8位，6位，4位，3位"""
    def __init__(self, arg):
        super(BirthSet, self).__init__()
        self.all = []
        self.set_all(arg)
    def set_all(self, s):
        if isinstance(s, str):
            self.all.append((1, s))
            if len(s) == 8:
                self.all += [(1, s[2:]), (1, s[4:]), (1, s[:4])]
                if s[4] == '0':
                    self.all.append((1, s[5:]))
        elif isinstance(s, list):
            for x in s:
                self.set_all(x)

# if __name__ == '__main__':
#     b = BirthSet(['19930201', '19951204'])
#     print(b.all)