# Watermark PDFs

# Task

Huawei contacted Dan about a requirement for damsmanager to watermark some PDFs with

   **Do Not Duplicate**

Dan wrote a python script to add the watermark (also kept in a PDF).

I created a python virtualenv and a script that invokes that virtualenv to run Dan's script.

damsmanager can be configured to call my script, passing it two arguments: path to input PDF and path to output PDF.

# Requirements

python 3.X

virtualenv

PyPDF2

VRR_SCA_watermark.pdf

The watermark must be a PDF with an alpha channel.

# Implementation

On lib-hydratail-staging

Install python3, virtualenv, and create watermark virtualenv

    su sysN
    rhn-channel -a -c epel6-x86_64
    yum install python34
    yum install python-virtualenv
    
    mkdir /usr/local/etc/watermark
    chown tomcat.tomcat watermark
    
    su - tomcat
    cd /usr/local/etc
    virtualenv -p python3 watermark
    cd watermark
    source bin/activate
    pip install --upgrade pip
    pip install PyPDF2

Copy into the virtualenv Dan's script and the watermark PDF

    cd /usr/local/etc/watermark
    cp <source>/VRR_SCA_watermark.pdf .
    cp <source>/pdf_watermarker4.py .

Install

    cp <source>?watermark.sh /usr/local/bin
    chmod 755 /usr/local/bin/watermark.sh

Test

    /usr/local/bin/watermark.sh /tmp/test.pdf /tmp/test1a.pdf

# Damsmanager

Configure damsmanager to call watermark.sh

# Scripts

watermark.sh

    #!/bin/sh
    
    DIR=/usr/local/etc/watermark
    
    # rhn-channel -a -c epel6-x86_64
    # yum install python34
    # yum install python-virtualenv
    #
    # virtualenv -p python3 $DIR
    # cd $DIR
    # cp <source>/VRR_SCA_watermark.pdf .
    # source bin/activate
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
    
    cd $DIR
    source bin/activate
    
    python pdf_watermarker4.py -i $input -o $output
