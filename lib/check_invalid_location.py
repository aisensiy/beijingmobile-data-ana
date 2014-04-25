# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import glob
import os
from numpy import sin, cos, sqrt, arctan2, radians
from datetime import datetime
from constants import location_related_header as header


def dateparser(datetime_s):
    return datetime.strptime(datetime_s, '%Y%m%d%H%M%S')


def cal_est_distance(lon1, lat1, lon2, lat2):
    rate = 97
    return rate * np.sqrt((lon1 - lon2) ** 2 + (lat1 - lat2) ** 2) * 1.4


def cal_distance(lon1, lat1, lon2, lat2):
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * arctan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance


def pickout_invalid_points(filename):
    df = pd.read_csv(
        filename, header=None, names=header,
        parse_dates=['start_time'], date_parser=dateparser)

    df2 = df[['user_id', 'lac', 'longitude', 'latitude', 'start_time']]
    df2.dropna(how='any', inplace=True)
    df2 = df2.sort_index(by='start_time')
    df2 = df2.reset_index()

    df2['distance'] = 0
    df2['time'] = 0
    df2['speed'] = 0

    for i in xrange(1, len(df2)):
        x1 = df2.ix[i - 1, 'longitude']
        y1 = df2.ix[i - 1, 'latitude']
        x2 = df2.ix[i, 'longitude']
        y2 = df2.ix[i, 'latitude']

        df2.ix[i, 'distance'] = cal_est_distance(x1, y1, x2, y2)
        df2.ix[i, 'time'] = df2.ix[i, 'start_time'] - df2.ix[i - 1, 'start_time']
        # 做一个平滑，为所有的时间间隔都加两分钟
        df2.ix[i, 'speed'] = \
            df2.ix[i, 'distance'] / (df2.ix[i, 'time'].seconds + 120) * 3600

    speed_thresh = 100
    invalid_locations = set()

    df['point'] = df.longitude.astype(str) + ' ' + df.latitude.astype(str)
    df2['point'] = df2.longitude.astype(str) + ' ' + df2.latitude.astype(str)

    for i in xrange(1, len(df2)):
        if df2.ix[i, 'speed'] > speed_thresh:
            if df2.ix[i - 1, 'point'] not in invalid_locations:
                invalid_locations.add(df2.ix[i, 'point'])

    df = df[~df.point.isin(invalid_locations)]
    df.start_time = df.start_time.map(lambda x: x.strftime('%Y%m%d%H%M%S'))
    del df['point']

    return df2, invalid_locations

if __name__ == '__main__':
    import sys
    # filename = '/Users/xushanchuan/data/userlog-20131202/00/102171900.csv'
    # df, locs = pickout_invalid_points(filename)
    targetroot = sys.argv[1]
    dstrootdir = "%s-no-invalidpoint" % targetroot

    if not os.path.isdir(dstrootdir):
        os.mkdir(dstrootdir)

    files = glob.glob(os.path.join(targetroot, '*', '*.csv'))
    for cnt, csvfile in enumerate(files):
        print '[%d] processing: %s' % (cnt, csvfile)
        uid = os.path.splitext(os.path.basename(csvfile))[0]
        dstdir = os.path.join(dstrootdir, uid[-2:])
        if not os.path.isdir(dstdir):
            os.mkdir(dstdir)

        df, invalid_locations = pickout_invalid_points(csvfile)
        df.to_csv(os.path.join(dstdir, uid + '.csv'), header=None, index=None)
        with open(os.path.join(dstdir, uid + '.point'), 'w') as ofile:
            for point in invalid_locations:
                ofile.write("%s\n" % point)
