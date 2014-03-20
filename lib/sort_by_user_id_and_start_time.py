#-*- coding: utf8 -*-

import pandas as pd
import sys
import common

# input is a raw unsorted log file
input_file = sys.argv[1]

# output is a log file sort by user_id and start_time
output_file = common.add_postfix(input_file, 'sortuidtime')

df = pd.read_csv(input_file)

# drop null values on longitude latitude and start_time
df = df[df.longitude.notnull() & df.latitude.notnull() & df.start_time.notnull()]


df = df.drop_duplicates()

df = df.sort_index(by=['user_id', 'start_time'])

df.to_csv(output_file, index=None, encoding='utf8')
