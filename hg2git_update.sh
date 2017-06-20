#!/bin/bash

unset source
unset target
source=$1
target=$2

if [[ -z $source ]] || [[ -z $target ]]; then
    echo "Please provide the paths to the original Hg repository and the Git repository you wish to update!"
    exit 1
fi

cd $target
./hg-fast-export.sh -r $source --force -A reformatted-authors.txt
