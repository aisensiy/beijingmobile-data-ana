#-*- coding: utf8 -*-

import common
import pandas as pd
import os
from constants import location_related_header as headers
from constants import locallist_headers
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

columns = ['user_id', 'location', 'start_time']

def generate_locationlist(inputfile, outputfile, mode):
    logging.info('From %s to %s with mode %s', inputfile, outputfile, mode)
    df = pd.read_csv(inputfile, header=None, names=headers,
            dtype={'start_time': str})

    # drop null values on longitude latitude and start_time
    df = df[df.longitude.notnull() & df.latitude.notnull() & df.start_time.notnull()]
    if len(df) == 0:
        logging.info('no valid record in %s', inputfile)
        return

    df = df.drop_duplicates()

    def format_float(col):
        return "%.4f" % col

    df['longitude'] = df['longitude'].apply(format_float)
    df['latitude'] = df['latitude'].apply(format_float)
    df['location'] = df['longitude'] + ' ' + df['latitude']

    df = df[columns]

    # sort by user_id and start_time
    df = df.sort_index(by=['user_id', 'start_time'])
    # 重置索引 索引再次成为 1 2 3 4 ...
    df = df.reset_index()

    grouped = df.groupby('user_id')

    result = grouped.agg({'user_id': 'max',
        'location': lambda x: list(x),
        'start_time': lambda x: list(x)})

    def zip_two_col_and_rm_duplicates(row):
        locations = zip(row['start_time'], row['location'])
        newlocations = []
        for start_time, location in locations:
            if len(newlocations) == 0:
                newlocations.append((start_time, location))
            elif newlocations[-1][1] != location:
                newlocations.append((start_time, location))
        return ','.join(["%s:%s" % (time, loc) for time, loc in newlocations])

    result['locations'] = result.apply(zip_two_col_and_rm_duplicates, axis=1)
    result['location_size'] = result['locations'].map(lambda x: len(x.split(',')))
    result['date'] = '2012-12-01'
    result = result[locallist_headers]
    result.to_csv(outputfile, index=None, encoding='utf8', mode=mode, header=None)

if __name__ == '__main__':
    import sys
    import glob

    # input is a raw log
    input_file = sys.argv[1]

    # output is a user list with locations order by time
    if len(sys.argv) >= 3 and len(sys.argv[2]) > 0:
        output_file = sys.argv[2]
        mode = "a"
    else:
        output_file = common.add_postfix(input_file, 'location_list')
        mode = "w"

    if os.path.isdir(input_file):
        files = glob.glob(os.path.join(input_file, '*', '*.csv'))
        for csvfile in files:
            generate_locationlist(csvfile, output_file, mode)
    else:
        generate_locationlist(input_file, output_file, mode)

