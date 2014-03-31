import sys
import os

# The inputfile should already sort by user_id so only need to open the
# $user_id.csv for one time
inputfile = sys.argv[1]
filemode = sys.argv[2]
dirname = 'userlog'
dirpath = os.path.dirname(inputfile)
dstdirname = os.path.join(dirpath, dirname)

if not os.path.isdir(dstdirname):
    os.mkdir(dstdirname)

with open(inputfile, 'r') as ifile:
    lastuid = None
    ofile = None
    for line in ifile:
        uid, other = line.split(',', 1)
        # If the uid changed, close old file and open a new one
        if lastuid != uid:
            if ofile: ofile.close()
            ofile = open(os.path.join(dstdirname, uid + ".csv"), filemode)
        lastuid = uid
        ofile.write(line)
