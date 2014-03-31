#-*- coding: utf8 -*-

import common
import sys
import pandas as pd
import os


headers = ['user_id', 'access_mode_id', 'logic_area_name', 'lac', 'ci',
           'longitude', 'latitude', 'busi_name', 'busi_type_name',
           'app_name', 'app_type_name', 'start_time',
           'up_pack', 'down_pack', 'up_flow', 'down_flow', 'site_name',
           'site_channel_name', 'cont_app_id', 'cont_classify_id',
           'cont_type_id', 'acce_url']

# input is a raw log
input_file = sys.argv[1]

# output is a user list with locations order by time
if len(sys.argv >= 3) and len(sys.argv[2]) > 0:
    output_file = sys.argv[2]
    mode = "a"
else:
    output_file = common.add_postfix(input_file, 'location_list')
    mode = "w"

print 'From %s to %s with mode %s' % (input_file, output_file, mode)

columns = ['user_id', 'location', 'start_time']

df = pd.read_csv(input_file, header=None, names=headers)

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

# print result.head()

def zip_two_col_and_rm_duplicates(row):
    locations = zip(row['start_time'], row['location'])
    newlocations = []
    for start_time, location in locations:
        if len(newlocations) == 0 or newlocations[-1][1] != location:
            newlocations.append((start_time, location))
    newlocations.sort()
    return ','.join(["%s:%s" % (time, loc) for time, loc in newlocations])

result['locations'] = result.apply(zip_two_col_and_rm_duplicates, axis=1)
# print result['locations'].head()

result['location_size'] = result['locations'].map(lambda x: len(x.split(',')))

result = result[['user_id', 'locations', 'location_size']]

# print len(result)
# print result.head()

result.to_csv(output_file, index=None, encoding='utf8', mode=mode, header=None)
