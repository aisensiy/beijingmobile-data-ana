#-*- coding: utf8 -*-

import common
import pandas as pd
import os
from constants import call_headers as headers
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

    def loc_column(row):
        return row['longitude'] + ' ' + row['latitude']

    df['location'] = df.apply(loc_column, axis=1)

    df = df[columns]

    # sort by user_id and start_time
    df = df.sort_index(by=['user_id', 'start_time'])
    df['date'] = df['start_time'].map(lambda x: x.split(' ')[0])
    df['start_time'] = df['start_time'].apply(
        lambda x: pd.to_datetime(x).strftime('%Y%m%d%H%M%S'))

    grouped = df.groupby(['user_id', 'date'])

    result = grouped.agg({
        'user_id': 'max',
        'date': 'max',
        'location': lambda x: '|'.join(x),
        'start_time': lambda x: '|'.join(x)})

    def zip_two_col_and_rm_duplicates(row):
        row['start_time'] = row['start_time'].split('|')
        row['location'] = row['location'].split('|')

        locations = zip(row['start_time'], row['location'])
        newlocations = []
        for start_time, location in locations:
            if len(newlocations) == 0 or newlocations[-1][1] != location:
                newlocations.append((start_time, location))
        newlocations.sort()
        return ','.join(["%s:%s" % (time, loc) for time, loc in newlocations])

    result['locations'] = result.apply(zip_two_col_and_rm_duplicates, axis=1)
    result['location_size'] = result['locations'].map(lambda x: len(x.split(',')))
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
        generate_locationlist(input_file, output_file)

