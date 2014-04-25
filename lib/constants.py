# -*- coding: utf8 -*-


log_headers = ['user_id', 'access_mode_id', 'logic_area_name', 'lac',
               'ci', 'longitude', 'latitude', 'busi_name',
               'busi_type_name', 'app_name', 'app_type_name', 'start_time',
               'up_pack', 'down_pack', 'up_flow', 'down_flow',
               'site_name', 'site_channel_name', 'cont_app_id', 'cont_classify_id',
               'cont_type_id', 'acce_url']

call_headers = ['user_id', 'target_id', 'start_time',
                'end_time', 'roam', 'basename',
                'longitude', 'latitude']

locallist_headers = ['user_id', 'locations', 'location_size', 'date']

location_related_header = ['user_id', 'lac', 'longitude', 'latitude',
                            'start_time']

merged_location_related_header = ['user_id', 'lac', 'longitude',
                                 'latitude', 'start_time', 'type']

db = {}
db['dev'] = {
        'host': 'localhost',
        'user': 'root',
        'passwd': '000000',
        'port': 3306,
        'charset': 'utf8',
        'db': 'chinamobile'
        }
db['product'] = {
        'host': 'localhost',
        'user': 'root',
        'passwd': '000000',
        'port': 3306,
        'charset': 'utf8',
        'db': 'chinamobile'
        }
