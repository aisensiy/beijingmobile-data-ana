#-*- coding: utf8 -*-

import common
import sys
import pandas as pd

# input is a raw log
input_file = sys.argv[1]
# userinfo file
userinfo_file = sys.argv[2]
# output is a user list with locations order by time
output_file = common.add_postfix(input_file, 'joineduser')

joinkey = 'user_id'
usekeys = ['user_id',
           'gprs_flow', 'gprs_fee', 'call_fee',
           'brand_chn', 'terminal_price',
           'dept_county_name', 'dept_name']

userdf = pd.read_csv(userinfo_file)
userdf = userdf[usekeys]

df = pd.read_csv(input_file)

merged = pd.merge(df, userdf, left_on="user_id", right_on="user_id", how="left")
merged = merged.drop_duplicates()

print merged.head()

merged.to_csv(output_file, index=None, encoding='utf8')

