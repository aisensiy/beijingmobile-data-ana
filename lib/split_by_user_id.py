import os

def split_by_user_id(filepath, dirpath):
    with open(filepath, 'r') as ifile:
        lastuid = None
        ofile = None
        for line in ifile:
            uid, other = line.split(',', 1)
            # If the uid changed, close old file and open a new one
            if lastuid != uid:
                if ofile: ofile.close()
                # put file in folder named by last two number
                folder = uid[-2:]
                folderpath = os.path.join(dirpath, folder)
                # create the folder if not exist
                if not os.path.isdir(folderpath):
                    os.mkdir(folderpath)
                ofile = open(os.path.join(folderpath, uid + ".csv"), filemode)
            lastuid = uid
            ofile.write(line)

if __name__ == '__main__':
    import sys
    # The inputfile should already sort by user_id so only need to open the
    # $user_id.csv for one time
    inputfile = sys.argv[1]
    dirname = sys.argv[2]
    filemode = sys.argv[3]
    dirpath = os.path.dirname(inputfile)
    dstdirname = os.path.join(dirpath, dirname)

    if not os.path.isdir(dstdirname):
        os.mkdir(dstdirname)

    split_by_user_id(inputfile, dstdirname)
