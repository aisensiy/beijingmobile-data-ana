#-*- coding: utf8 -*-

import common
import sys
import pandas as pd

# input is a raw log
input_file = sys.argv[1]
# output is a user list with locations order by time
output_file = common.add_postfix(input_file, 'loclist')

print 'From %s to %s' % (input_file, output_file)

columns = ['user_id', 'location']

df = pd.read_csv(input_file)

df = df[df.longitude.notnull() & df.latitude.notnull()]

def loc_column(row):
    return str(row['longitude']) + ' ' + str(row['latitude'])

df['location'] = df.apply(loc_column, axis=1)

print df['location'].head()

df = df[columns]

grouped = df.groupby('user_id')

def rm_duplicated_location(locations):
    newlocations = []
    for location in locations:
        if len(newlocations) == 0 or newlocations[-1] != location:
            newlocations.append(location)
    return ','.join(newlocations)

result = grouped.agg({'user_id': 'max', 'location': rm_duplicated_location})
result['location_size'] = result['location'].map(lambda x: len(x.split(',')))

print len(result)
print result.head()

result.to_csv(output_file, index=None, encoding='utf8')
