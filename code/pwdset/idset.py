# 用来处理ID类（身份证、工号、学号）

class IdSet(object):
    """docstring for IdSet"""
    def __init__(self, arg):
        super(IdSet, self).__init__()
        self.all = []
        self.set_all(arg)
    def set_all(self, s):
        if isinstance(s, str):
            # 如果是身份证则增加倒数7-2位选项
            if len(s) == 18:
                s = s.lower()
                self.all.append((3, s[-7:-1]))
            if len(s) >= 6:
                self.all.append((1, s[-6:]))
            if len(s) >= 8:
                self.all.append((1, s[-8:]))
            if len(s) != 6 and len(s) != 8:
                self.all.append((2, s))
        elif isinstance(s, list):
            for x in s:
                self.set_all(x)

# if __name__ == '__main__':
#     i = IdSet(['123', '21341212345'])
#     # i = IdSet('330220199909122345')
#     print(i.all)
