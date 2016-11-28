import re
import hashlib
import zipfile
import os
from pwdset import *

def md5gen(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def evil_filter(s):
    s = s.replace('，', ',').replace('＋', '+').replace('－', '-')
    rex = re.compile('[^a-zA-Z0-9_,@+\.\-\s]+')
    return rex.sub('', s).split(',')

def num_filter(s):
    rex = re.compile('[^0-9]+')
    return rex.sub('', s)

def keys_merge(*args):
    result = args[0]
    for s in args[1:]:
        t = []
        for r in result:
            for x in s:
                k = r[1] + x[1]
                # 增加长度影响因子
                w = int(r[0] * x[0] * len(k) / 5)
                t.append((w, k))
        result = t 
    return result

def len_limit(val, min_len = 6, max_len = 16):
    return [x[1].strip() for x in val if min_len <= len(x[1].strip()) <= max_len]

class Person(object):
    """docstring for Person"""
    def __init__(self, kws, level, min_len):
        self.kws     = kws
        self.level   = level
        self.min_len = min_len
        self.ext     = ExtSet()
        self.set_pwd(kws)
        self.set_passwd(level)
    def set_pwd(self, val):
        # 过滤中文和特殊字符
        kws = {k: evil_filter(v) for k, v in val.items()}
        self.ids    = IdSet(kws.get('idcard', []) + kws.get('uid', [])).all
        self.cnames = CnameSet(kws.get('cname', [])).all
        self.enames = EnameSet(kws.get('ename', [])).all
        self.tels   = TelSet(kws.get('phone', []) + kws.get('tel', []) + kws.get('qq', [])).all
        self.keys   = KeySet(kws.get('wechat', []) + kws.get('email', []) + kws.get('others', [])).all
        self.birth  = BirthSet(kws.get('birthday', [])).all
        self.words  = self.cnames + self.enames + self.keys
        self.nums   = self.ids + self.tels + self.birth
        # 过滤非数字，常用默认密码，只限制最短长度
        self.pwd    = [num_filter(x[1]) for x in sorted(self.nums) if len(num_filter(x[1])) >= self.min_len]
    def set_passwd(self, level):
        switcher = {
            1: self.words + self.nums,
            2: keys_merge(self.words, self.nums),
            3: keys_merge(self.words, self.ext.num_ext) +
                keys_merge(self.nums, self.ext.str_ext) +
                keys_merge(self.ext.str_ext, self.nums),
            4: keys_merge(self.words, self.nums, self.ext.char_ext) +
                keys_merge(self.ext.str_ext, self.nums, self.ext.char_ext) +
                keys_merge(self.nums + self.words)
        }
        merged_keys = []
        for x in range(level):
            merged_keys += switcher.get(x + 1)
        self.passwd = merged_keys

class PassGen(object):
    """docstring for PassGen"""
    def __init__(self, kws):
        super(PassGen, self).__init__()
        self.kws = kws
        self.min_len = int(kws.get('minlen', 6))
        self.max_len = int(kws.get('maxlen', 16))
        self.level = int(kws.get('level', 4))
        self.pa = Person(self.get_main_kws(), self.level, self.min_len)
        self.ta = Person(self.get_ta_kws(), self.level, self.min_len)
        self.love_ext = ExtSet().love_ext
        self.love_and = ExtSet().love_and
        self.set_top_passwd()
        self.set_passwd()
        self.save_file()
    def get_main_kws(self):
        return {
            'idcard': self.kws.get('idcard', ''),
            'uid': self.kws.get('uid', ''),
            'cname': self.kws.get('cname', ''),
            'ename': self.kws.get('ename', ''),
            'phone': self.kws.get('phone', ''),
            'tel': self.kws.get('tel', ''),
            'qq': self.kws.get('qq', ''),
            'wechat': self.kws.get('wechat', ''),
            'email': self.kws.get('email', ''),
            'birthday': self.kws.get('birthday', ''),
            'others': self.kws.get('others', '')
        }
    def get_ta_kws(self):
        return {
            'cname': self.kws.get('tacname', ''),
            'ename': self.kws.get('taename', ''),
            'phone': self.kws.get('taphone', ''),
            'birthday': self.kws.get('tabirthday', '')
        }
    def set_top_passwd(self):
        top_passwd = []
        try:
            with open('/root/code/top_passwd.txt', 'r') as f:
                for x in range(self.level * 50):
                    top_passwd.append((3, f.readline().strip()))
        except:
            print('Get top password file error')
        self.top_passwd = top_passwd
    def set_passwd(self):
        love_passwd = keys_merge(self.ta.words, self.love_ext) + keys_merge(self.love_ext, self.ta.words) + keys_merge(self.pa.words, self.love_and, self.ta.words)
        merged_keys = self.pa.passwd + self.ta.passwd + love_passwd + self.top_passwd
        passwd = self.pa.pwd + len_limit(sorted(merged_keys), self.min_len, self.max_len)
        if self.level == 0:
            passwd = [num_filter(x) for x in passwd if self.min_len <= len(num_filter(x)) <= self.max_len]
        self.passwd = sorted(set(passwd), key = passwd.index)
    def save_file(self):
        os.chdir('/root/code')
        print(os.getcwd())
        file_seed = ''.join(self.kws.values())
        print(file_seed)
        file_txt = 'password.txt'
        file_zip = './zip/' + md5gen(file_seed) + '.zip'
        try:
            with open(file_txt, 'w') as f:
                for x in self.passwd:
                    f.write(x + '\n')
        except:
            print('write password error')
        try:
            zf = zipfile.ZipFile(file_zip, 'w', zipfile.ZIP_DEFLATED)
            zf.write(file_txt)
        except:
            print('zip error')
        finally:
            zf.close()
        os.remove(file_txt)
        self.filelink = file_zip[1:]
