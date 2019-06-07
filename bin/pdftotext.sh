#!/bin/sh

# set flag vars to empty, or set a default value

filepath=
tmp_dir=
target_dir=
out=
dpi="600"
file_prefix="file"
language="eng"

while [ $# -gt 0 ]
do
    case $1 in
	-f | --filepath) filepath=$2
	    shift
	    ;;
	-t | --targetdir) target_dir=$(realpath -e $2)
	    shift
	    ;;
	-p | --tmp) tmp_dir=$(realpath -e $2)
	    shift
	    ;;
	-o | --output) out=$2
	    shift
	    ;;
	--dpi) dpi=$2
	    shift
	    ;;
	--prefix) file_prefix=$2
	    shift
	    ;;
	--language) language=$2
	    shift
	    ;;
    esac

    shift
done


out=$(realpath -m $target_dir/$out)

pdftoppm $filepath -r $dpi $tmp_dir/$file_prefix

for i in $tmp_dir/*ppm; do

    filename=$tmp_dir/`basename "$i" .ppm`
    tiffile=$filename.tif
    convert $i $tiffile && rm $i

    tesseract $tiffile $filename -l $language
    rm $tiffile

    cat "$filename.txt" |
    tr '\t\n\v\r' ' ' |
    tr -s ' ' |
	sed 's/\([.!?]\)[[:space:]]\([[:upper:][:punct:][:digit:]]\)/\1\n\2/g' >> "$out"

    rm "$filename.txt"
    
done

exit 0
