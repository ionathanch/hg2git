#!/bin/bash

set -e

unset source
unset target
unset authors
unset fast_export

source=$1
target=$2
authors=$3
fast_export=$4

if [[ -z $source ]] || [[ -z $target ]] || [[ -z $authors ]] || [[ -z $fast_export ]]; then
    echo "Some paths have not been set. Please provide all of the following: <source> <target> <authors> <fast_export>"
    exit 1
fi

echo "Downloading hg-fast-export..."
rm -rf $fast_export
git clone --depth=1 --branch=master https://github.com/frej/fast-export.git $fast_export

echo "Copying authors.py and users.csv..."
mkdir -p $authors && cp {authors.py,users.csv} $authors

echo "Creating a list of authors from existing repository users..."
mkdir -p $target
cd $source
hg log | grep user: | sort | uniq | sed "s/user: *//" > $target/authors.txt
cd $target
python $authors/authors.py

echo "Starting export with hg-fast-export..."
cp $fast_export/* .
git init
git config core.ignoreCase false
./hg-fast-export.sh -r $source --force -A reformatted-authors.txt
git config --bool core.bare true

echo "All done! If you want to update this Git repository from the Hg repository, DO NOT DELETE ANY FILES FROM $target!!"
echo "To update this Git repository, run the hg2git_update.sh script."
echo "If you are absolutely sure you won't need to update this Git repository again, run the hg2git_clean.sh script to clean everything up."
echo "This script will strip large files, tag and delete closed branches, create .gitignore files, and delete temporary files."
