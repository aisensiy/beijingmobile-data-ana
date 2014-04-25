# -*- coding: utf-8 -*-
import pandas as pd
import os
import glob
from constants import location_related_header as loc_header
from constants import log_headers


if __name__ == '__main__':
    import sys
    print sys.argv[1]
    if os.path.isdir(sys.argv[1]):
        files = glob.glob(os.path.join(sys.argv[1], '*', '*.csv'))
        for csvfile in files:
            print 'processing: %s' % csvfile
            filename = os.path.basename(csvfile)
            foldername = os.path.splitext(filename)[0][-2:]
            folderpath = os.path.join(sys.argv[2], foldername)
            if not os.path.isdir(folderpath):
                os.mkdir(folderpath)
            dstfile = os.path.join(folderpath, filename)
            df = pd.read_csv(csvfile, header=None, names=log_headers)
            df[loc_header].to_csv(dstfile, index=None, header=None)
    else:
        print 'No dir is given'
