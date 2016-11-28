# 手机电话QQ号等电信属性的编号

class TelSet(object):
    """手机QQ电话等"""
    def __init__(self, arg):
        super(TelSet, self).__init__()
        self.all = []        
        self.set_all(arg)
    def set_all(self, s):
        if isinstance(s, str):
            self.all.append((1, s))
        elif isinstance(s, list):
            for x in s:
                self.set_all(x)


# if __name__ == '__main__':
#     t = TelSet(['13209876546', '07812342345'])
#     print(t.all)