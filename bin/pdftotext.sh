#!/bin/sh

# set flag vars to empty, or set a default value

filepath=
target_dir=
out=
dpi=600
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

pdftoppm $filepath -r $dpi $target_dir/$file_prefix

for i in $target_dir/*ppm; do

    filename=$target_dir/`basename "$i" .ppm`
    tifile=$filename.tif

    convert $i $tifile && rm $i

    tesseract $tifile -l $language $filename && rm $tifile

    cat "$filename.txt" |
    tr '\t\n\v\r' ' ' |
    tr -s ' ' |
	sed 's/\([.!?]\)[[:space:]]\([[:upper:][:punct:][:digit:]]\)/\1\n\2/g' >> "$out.txt"

    # cat "$filename.txt" >> $out && rm "$filename.txt";
    
    rm "$filename.txt"
    
done

exit 0
