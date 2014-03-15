filename=$1
uid=$2
head -1 $filename
grep ^$2, $filename
