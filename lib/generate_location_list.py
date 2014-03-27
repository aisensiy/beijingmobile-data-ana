#-*- coding: utf8 -*-

import common
import sys
import pandas as pd

# input is a raw log
input_file = sys.argv[1]
# output is a user list with locations order by time
output_file = common.add_postfix(input_file, 'location_list')

print 'From %s to %s' % (input_file, output_file)

columns = ['user_id', 'location', 'start_time']

df = pd.read_csv(input_file)

def loc_column(row):
    return str(row['longitude']) + ' ' + str(row['latitude'])

df['location'] = df.apply(loc_column, axis=1)

print df['location'].head()

df = df[columns]

# sort by user_id and start_time
df = df.sort_index(by=['user_id', 'start_time'])

grouped = df.groupby('user_id')

result = grouped.agg({'user_id': 'max',
    'location': lambda x: list(x),
    'start_time': lambda x: list(x)})

print result.head()

def zip_two_col_and_rm_duplicates(row):
    locations = zip(row['start_time'], row['location'])
    newlocations = []
    for start_time, location in locations:
        if len(newlocations) == 0 or newlocations[-1][1] != location:
            newlocations.append((start_time, location))
    newlocations.sort()
    return ','.join(["%s:%s" % (time, loc) for time, loc in newlocations])

result['locations'] = result.apply(zip_two_col_and_rm_duplicates, axis=1)
print result['locations'].head()

result['location_size'] = result['locations'].map(lambda x: len(x.split(',')))

result = result[['user_id', 'locations', 'location_size']]

print len(result)
print result.head()

result.to_csv(output_file, index=None, encoding='utf8')
