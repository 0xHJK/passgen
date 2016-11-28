# 微信号 用户名 关键字

class KeySet(object):
    """微信号，用户名，关键字"""
    def __init__(self, arg):
        super(KeySet, self).__init__()
        self.all = []
        self.set_all(arg)
    def set_all(self, s):
        if isinstance(s, str):
            if s.find('@') > 0:
                self.all.append((1, s.split('@')[0]))
            else:
                self.all.append((1, s))
        elif isinstance(s, list):
            for x in s:
                self.set_all(x)

# if __name__ == '__main__':
#     k = KeySet(['sdff32f', '12sa@1s.com', '213sad'])
#     print(k.all)

