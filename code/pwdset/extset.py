class ExtSet(object):
    """可以理解为配置文件"""
    def __init__(self):
        super(ExtSet, self).__init__()
        self.num_ext = [(2, '123'), (2, '1234'), (2, '12345'), (2, '123456'), 
            (2, '321'), (2, '123321'), (2, '123123'), (2, '233'), (2, '666'), (2, '1024'), 
            (2, '2016'), (2, '2015'), (2, '2014'), (3, '2008')]
        self.str_ext_low    = [(2, 'a'), (2, 'q'), (2, 'x'), (2, 'z'), (2, 'qq'), (2, 'aa'), 
            (2, 'xx'), (2, 'abc'), (2, 'aaa'), (2, 'asd'), (2, 'qwe'), (3, 'zxc')]
        self.str_ext_up = [(x[0]+1, x[1].upper()) for x in self.str_ext_low]
        self.str_ext = self.str_ext_low + self.str_ext_up
        self.char_ext   = [(3, '.'), (3, '..'), (3, '...'), (3, '*'), 
            (3, '**'), (3, '@'), (3, '!'), (3, '%')]
        self.love_ext   = [(3, '520'), (3, '1314'), (3, '5201314'), (3, 'love')]
        self.love_and = [(3, 'love'), (4, 'ai')]

if __name__ == '__main__':
    e = ExtSet()
    print(e.str_ext)
    