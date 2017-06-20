#!/bin/bash

unset source
unset target
unset bfg_cleaner

source=$1
target=$2
bfg_cleaner=$3

if [[ -z $source ]] || [[ -z $target ]] || [[ -z $bfg_cleaner ]]; then
    echo "Some paths have not been set. Please provide all of the following: <source> <target> <bfg_cleaner>"
    exit 1
fi

echo "Stripping out large files with BFG Repo-Cleaner..."
mkdir -p $bfg_cleaner
curl "http://repo1.maven.org/maven2/com/madgag/bfg/1.12.15/bfg-1.12.15.jar" -o $bfg_cleaner/bfg.jar
java -jar $bfg_cleaner/bfg.jar --strip-blobs-bigger-than 40M $target
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "Tagging and deleting closed branches..."
cd $source
hg heads --closed --template "{branch}\n" | tr " " "_" | sort > $target/all.log
hg heads          --template "{branch}\n" | tr " " "_" | sort > $target/open.log
cd $target
comm -2 -3 all.log open.log > closed.log
for branch in `cat closed.log`; do git tag "closed/$branch" $branch; git branch -df $branch; done

# TODO: Loop this for each open branch
echo "Creating .gitignore files from .hgignore files..."
find . -name ".hgignore" > hgignore-files.log
touch gitignore-files.log
for file in `cat hgignore-files.log`; do
    newfile=${file/hgignore/gitignore};
    echo $newfile >> gitignore-files.log
    cp $file $newfile;
    sed -i.bak "s/syntax:/#syntax:/; s/^\^//; s/\$$//; s/\\\w\+/*/; s/\\\\\//\//g" $newfile;
done

echo "All done! This Git repository is now ready to be pushed after the .gitignore files have been committed to the desired branches."
