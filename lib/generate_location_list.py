#-*- coding: utf8 -*-

import common
import sys
import pandas as pd
import os
import glob
from constants import log_headers as headers
from constants import locallist_headers

# input is a raw log
input_file = sys.argv[1]

# output is a user list with locations order by time
if len(sys.argv) >= 3 and len(sys.argv[2]) > 0:
    output_file = sys.argv[2]
    mode = "a"
else:
    output_file = common.add_postfix(input_file, 'location_list')
    mode = "w"

columns = ['user_id', 'location', 'start_time']

def generate_locationlist(inputfile, outputfile, mode):
    print 'From %s to %s with mode %s' % (inputfile, outputfile, mode)
    df = pd.read_csv(inputfile, header=None, names=headers)
    def loc_column(row):
        return str(row['longitude']) + ' ' + str(row['latitude'])

    df['location'] = df.apply(loc_column, axis=1)

    df = df[columns]

    # sort by user_id and start_time
    df = df.sort_index(by=['user_id', 'start_time'])

    grouped = df.groupby('user_id')

    result = grouped.agg({'user_id': 'max',
        'location': lambda x: list(x),
        'start_time': lambda x: list(x)})

    def zip_two_col_and_rm_duplicates(row):
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
    if os.path.isdir(input_file):
        files = glob.glob(os.path.join(input_file, '*', '*.csv'))
        for csvfile in files:
            generate_locationlist(csvfile, output_file, mode)
    else:
        generate_locationlist(input_file, output_file)

