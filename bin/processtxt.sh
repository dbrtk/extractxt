#!/bin/sh

# set flag vars to empty, or set a default value

filepath=
target_dir=
out=

while [ $# -gt 0 ]
do
    case $1 in
	-f | --filepath) filepath=$2
	    shift
	    ;;
	-t | --targetdir) target_dir=$(realpath -e $2)
	    shift
	    ;;
	-o | --output) out=$2
	    shift
	    ;;
    esac
    shift
done

out=$(realpath -m $target_dir/$out)

cat "$filepath" |
    tr '\n' ' ' |
    tr -s ' ' |
    sed 's/\([.!?]\)[[:space:]]\([[:upper:][:punct:][:digit:]]\)/\1\n\2/g' >> "$out.txt"

exit 0

