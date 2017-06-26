# Mercurial to Git Migration
These scripts will migrate a Mercurial repository to a Git repository using hg-fast-export, strip large files using BFG Repo-Cleaner, tag and delete branches that were closed in Mercurial, and convert .hgignore files to .gitignore files.

## Notes
* If any .sh scripts cannot be executed, replace `./` with `bash ` or execute `chmod u+x <.sh script>`.
* The scripts require some of the following arguments:
    * `<source>`: The Mercurial repository that you are migrating **FROM**.
    * `<target>`: The Git repository that you are mirating **TO**.
    * `<authors>`: The directory to which authors.py and users.csv will be copied. 
    * `<fast-export>`: The directory to which https://github.com/frej/fast-export will be cloned. All files in this directory will be overwritten.
    * `<bfg-cleaner>`: The directory to which the BFG Repo-Cleaner .jar file will be downloaded.

## Instructions
1. Copy all hg2git\*.sh, authors.py, and users.csv files to the same directory.
2. Run `./hg2git.sh <source> <target> <authors> <fast-export>`. This may take a while. Do **NOT** delete the reformatted-authors.txt file.
3. If you have new changes in your Mercurial repository and you wish to update your Git repository, ensure the changes have been pulled (`hg pull`) and run `./hg2git_update.sh <source> <target>`. 
4. Before moving on, make sure that you are **absolutely sure** you no longer need to update your Git repository from your Mercurial repository. Once you perform the next steps, you **cannot** update again.
5. To strip out large files from history and delete closed branches, run `./hg2git_clean.sh <source> <target> <bfg-cleaner>`. Files larger than 40M will be stripped. This may take a while.
6. To copy .hgignore files to .gitignore, convert _some_ of the regex to globs, and commit these files for every branch, run `./hg2git_ignore.sh <target>`. Note that this will convert the repository from bare to non-bare and check out files.
7. Set an upstream (`git remote add origin <url>`) and push the repository (`git push --all origin -u`). This may take a while.
8. To remove temporary files that were created during the execution of these scripts (.bak, .log, \*authors.txt, hg-fast-export files), run `git clean -df`. 

## TL;DR
1. `./hg2git.sh <source> <target> <authors> <fast-export>`
2. `./hg2git_update.sh <source> <target>`
3. Read [Instructions](#instructions) > Step 4.
4. `./hg2git_clean.sh <source> <target> <bfg-cleaner>`
5. `./hg2git_ignore.sh <target>`
6. `git remote add origin <url> && git push --all origin -u`
7. `git clean -df`
