#!/bin/bash

set -e

unset $target
target=$1

if [[ -z $target ]]; then
    echo "Please provide the path to the desired Git repository!"
    exit 1
fi

echo "Creating and committing .gitignore files for each branch..."
cd $target
git config --bool core.bare false
for branch in `git branch | sed "s/*/ /g"`; do
    git checkout $branch -f
    find . -name ".hgignore" > hgignore-files.log
    > gitignore-files.log
    for file in `cat hgignore-files.log`; do
        newfile=${file/hgignore/gitignore}
        echo $newfile >> gitignore-files.log
        cp $file $newfile
        sed -i.bak "s/syntax:/#syntax:/; s/^\^//; s/\$$//; s/\\\w\+/*/; s/\\\\\//\//g" $newfile
    done
    cat gitignore-files.log | xargs git add 
    if [[ -s gitignore-files.log ]]; then
        git commit -m "Added .gitignore files."
    fi
done

echo "All done! This Git repo is now ready to be pushed."
