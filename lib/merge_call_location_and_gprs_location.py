# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np
import logging
from datetime import datetime
from constants import location_related_header
from constants import call_headers
from constants import log_headers


def date_range(date):
    return ['%s 00:00:00' % date, '%s 23:59:59' % date]


def preparegprsdf(gprsfilename):
    gprs_df = pd.read_csv(gprsfilename, header=None,
                          names=location_related_header,
                          dtype={'start_time': str})
    gprs_df = gprs_df[gprs_df.longitude.notnull() & \
                      gprs_df.latitude.notnull() &
                      gprs_df.start_time.notnull()]
    gprs_df['type'] = 0

    return gprs_df


def preparecalldf(callfilename, date):
    call_df = pd.read_csv(callfilename, header=None, names=call_headers,
                          parse_dates=['start_time'])

    leftbound, rightbound = date_range(date)

    call_df = call_df[call_df.longitude.notnull() & \
                      call_df.latitude.notnull() &
                      call_df.start_time.notnull()]

    call_df = call_df[(call_df.start_time >= leftbound) & \
                      (call_df.start_time <= rightbound)]

    call_df['start_time'] = call_df['start_time'] \
        .map(lambda x: x.to_datetime().strftime('%Y%m%d%H%M%S'))

    for col in location_related_header:
        if col not in call_df.columns:
            call_df[col] = np.nan

    call_df = call_df[location_related_header]
    call_df['type'] = 1

    return call_df


def mergecsv(gprsfilename, callfilename, date):
    gprs_df = preparegprsdf(gprsfilename)
    call_df = preparecalldf(callfilename, date)

    df = pd.concat([call_df, gprs_df], ignore_index=True)
    df = df.sort_index(by='start_time')

    return df


if __name__ == '__main__':
    import sys
    import glob

    gprsfiledir = sys.argv[1]
    callfiledir = sys.argv[2]
    targetdir = sys.argv[3]
    date = sys.argv[4]

    if not os.path.isdir(targetdir):
        os.mkdir(targetdir)

    files = glob.glob(os.path.join(gprsfiledir, '*', '*.csv'))

    for gprsfile in files:
        print 'processing %s' % gprsfile
        uid = os.path.splitext(os.path.basename(gprsfile))[0]
        print 'uid: %s' % uid
        callfile = os.path.join(callfiledir, uid[-2:], uid + '.csv')

        targetfiledir = os.path.join(targetdir, uid[-2:])

        # 不重复生成合并文件
        if os.path.isdir(os.path.join(targetfiledir, uid + '.csv')):
            continue

        if os.path.isfile(callfile) and os.path.isfile(gprsfile):
            df = mergecsv(gprsfile, callfile, date)
        if not os.path.isfile(callfile):
            df = preparegprsdf(gprsfile)
        elif not os.path.isfile(gprsfile):
            df = preparecalldf(callfile, date)

        if not os.path.isdir(targetfiledir):
            os.mkdir(targetfiledir)

        df.to_csv(os.path.join(targetfiledir, uid + '.csv'),
                  index=None, header=None)

