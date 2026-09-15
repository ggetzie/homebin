#! /usr/bin/env bash

# the input is a file name - get the file name without the extension
input_file=$1
filename="${input_file%.*}"
echo "Processing $input_file"
# -resize 2400x3000 -units PixelsPerInch -density 300 -quality 100
magick "${input_file}" -colorspace Gray -sigmoidal-contrast 10,50% -negate -level 10%,90% "${filename}_cyano.png"