# -*- coding: utf8 -*-

import os
import common
import pandas as pd
import sys

file_name = sys.argv[1]
header_file_name = sys.argv[2]
dst_file_name = common.add_postfix(file_name, 'witheader')

def get_header_from_xlsx(filename):
    df = pd.read_excel(filename, 'Sheet1')
    df[u'字段编码'] = df[u'字段编码'].apply(lambda x: x.lower())
    return df[u'字段编码'].values

if __name__ == '__main__':
    headers = get_header_from_xlsx(header_file_name)
    df = pd.read_csv(file_name, header=None, chunksize=5000)
    with open(dst_file_name, 'w') as dstfile:
        dstfile.write(','.join(headers) + '\n')

    for chunk in df:
        chunk.to_csv(dst_file_name, mode='a', header=None, index=None)
