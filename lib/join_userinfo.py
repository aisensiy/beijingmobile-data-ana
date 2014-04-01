#-*- coding: utf8 -*-

import common
import pandas as pd
from constants import locallist_headers

def join_userinfo_with_locallist(locallist, userinfo):
    joinkey = 'user_id'
    usekeys = ['user_id',
               'gprs_flow', 'gprs_fee', 'call_fee',
               'brand_chn', 'terminal_price',
               'dept_county_name', 'dept_name']

    userdf = pd.read_csv(userinfo)
    userdf = userdf[usekeys]

    df = pd.read_csv(locallist, names=locallist_headers)

    merged = pd.merge(df, userdf, left_on="user_id", right_on="user_id", how="left")
    merged = merged.drop_duplicates()

    return merged

if __name__ == '__main__':
    import sys
    # input is a raw log
    input_file = sys.argv[1]
    # userinfo file
    userinfo_file = sys.argv[2]
    # output is a user list with locations order by time
    output_file = common.add_postfix(input_file, 'join_userinfo')

    merged = join_userinfo_with_locallist(input_file, userinfo_file)
    merged.to_csv(output_file, index=None, encoding='utf8')
