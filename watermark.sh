#!/bin/sh

DIR=/usr/local/etc/watermark

# rhn-channel -a -c epel6-x86_64
# yum install python34
# yum install python-virtualenv
#
# virtualenv -p python3 $DIR
# cd $DIR
# source bin/activate
# pip install --upgrade pip
# cp <source>/VRR_SCA_watermark.pdf .
# cp <source>/pdf_watermark.py .
# pip install PyPDF2

if [ $# -ne 2 ]; then
  echo "usage: $0 <input pdf> <output pdf>"
  exit 1
fi
input=$1
output=$2

if [ ! -f $input ]; then
  echo "doesn't exist $input"
  exit 1
fi

if [ -f $output ]; then
  echo "already exists $output"
  exit 1
fi

if ! cd $DIR; then
  exit 1
fi
source bin/activate

python pdf_watermarker4.py -i $input -o $output 
res=$?

exit $res
