inputfile=$1
dirname=$(dirname $1)
cd $dirname
if [ ! -d "userlog" ]; then
  mkdir userlog
fi
gawk -F, '{print > "userlog/"$1".csv"}' $1
