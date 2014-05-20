#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import os
import glob
import sys

"""
把 id 相同的文件合并, 保证同一个 id 的文件只保留一个

从00文件开始，每遇到一个userid如果这个userid还没有出现在结果集中
就把这个userid的所有文件合并
"""

targetdir = sys.argv[1]
fromdir = sys.argv[2]
template = 'userlog-2013120%d-merged-no-invalidpoint'
date_range = range(2, 9)

def merge_files(useridfile):
    """@todo: Merge file split by date to one file

    :useridfile: the file name 1231231.csv
    :returns: None

    """
    middir = os.path.splitext(useridfile)[0][-2:]

    targetmiddir = os.path.join(targetdir, middir)
    if not os.path.isdir(targetmiddir): os.mkdir(targetmiddir)

    targetfile = os.path.join(targetdir, middir, useridfile)
    if os.path.isfile(targetfile): return

    splited_files = [os.path.join(fromdir, template % date, middir, useridfile)
                     for date in date_range]
    splited_files = filter(os.path.isfile, splited_files)

    print 'Merging file %s with %d files' % (useridfile, len(splited_files))

    with open(targetfile, 'w') as ofile:
        for splited_file in splited_files:
            for line in open(splited_file):
                ofile.write(line)

if not os.path.isdir(targetdir):
    os.mkdir(targetdir)

for date in date_range:
    dirname = os.path.join(fromdir, template % date)
    for i in range(100):
        files = glob.glob(os.path.join(dirname, ('%02d' % i), '*.csv'))
        useridfiles = map(os.path.basename, files)
        for useridfile in useridfiles:
            if os.path.isfile(os.path.join(targetdir, useridfile)):
                continue
            merge_files(useridfile)
