# -*- coding: utf-8 -*-

import re

def ip_convert(subject):
    ch_num = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    new_subject = []
    for i in subject:
        if re.search('\d+', i):
            new_subject.append(ch_num[int(i)])
        else:
           new_subject.append(i)
           continue
    return ''.join(new_subject)
