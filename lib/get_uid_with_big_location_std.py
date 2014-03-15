import common
import sys
import pandas as pd

filename = sys.argv[1]
thresh   = float(sys.argv[2])
dstfilename = common.add_postfix(filename, 'loc_with_std_' + sys.argv[2])

print 'start reading file %s' % filename
df = pd.read_csv(filename)

longitude_std = df.groupby('user_id')['longitude'].std()
valid_user_ids = list(longitude_std[longitude_std > thresh].index)

print 'valid by longitude: %s' % len(valid_user_ids)

df = df[df.user_id.isin(valid_user_ids)]
latitude_std = df.groupby('user_id')['latitude'].std()
valid_user_ids = list(latitude_std[latitude_std > thresh].index)

print 'valid by longitude and latitude: %d' % len(valid_user_ids)

df = df[df.user_id.isin(valid_user_ids)]
print 'start writing file %s' % dstfilename
df.to_csv(dstfilename, indes=None, encoding='utf8')
