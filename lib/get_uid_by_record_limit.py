#-*- coding: utf8 -*-

import sys
import pandas as pd
import common
import os

filename = sys.argv[1]
limit = int(sys.argv[2])
dstfilename = common.add_postfix(filename, 'with_record_size_limit_' + sys.argv[2])


if __name__ == '__main__':
    df = pd.read_csv(filename, chunksize=50000)
    isFirst = True

    if os.path.isfile(dstfilename):
        os.remove(dstfilename)

    for idx, chunk in enumerate(df):
        print idx
        grpsize = chunk.groupby('user_id').size()
        valid_user_ids = grpsize[grpsize >= limit]
        df2 = chunk[chunk.user_id.isin(list(valid_user_ids.index))]
        if isFirst:
            df2.to_csv(dstfilename, encoding='utf8', index=None, mode='a')
            isFirst = False
        else:
            df2.to_csv(dstfilename, encoding='utf8', index=None, header=None, mode='a')

