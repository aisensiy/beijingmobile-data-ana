filename=$1
cat $1 | sort --field-separator=',' --key=1
