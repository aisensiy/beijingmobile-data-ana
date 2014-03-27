#-*- coding: utf8 -*-

import pandas as pd
import sys
import common

headers = ['user_id', 'access_mode_id', 'logic_area_name', 'lac', 'ci',
           'longitude', 'latitude', 'busi_name', 'busi_type_name',
           'app_name', 'app_type_name', 'start_time',
           'up_pack', 'down_pack', 'up_flow', 'down_flow', 'site_name',
           'site_channel_name', 'cont_app_id', 'cont_classify_id',
           'cont_type_id', 'acce_url']


def sort_by_user_id_and_start_time(df):
    df.columns = headers

    del df['logic_area_name']
    del df['lac']
    del df['ci']

    # drop null values on longitude latitude and start_time
    df = df[df.longitude.notnull() & df.latitude.notnull() & df.start_time.notnull()]

    df = df.drop_duplicates()

    df = df.sort_index(by=['user_id', 'start_time'])

    return df

if __name__ == '__main__':
    # input is a raw unsorted log file
    input_file = sys.argv[1]
    # output is a log file sort by user_id and start_time
    output_file = common.add_postfix(input_file, 'sort_by_user_id_and_start_time')

    df = pd.read_csv(input_file, header=None, na_values=[''])
    df = sort_by_user_id_and_start_time(df)
    df.to_csv(output_file, index=None, encoding='utf8')

