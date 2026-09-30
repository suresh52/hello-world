#!/bin/bash

# set -x  # enable xtrace option
set -e  # Exit the script in case an error occurs

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
prj_dir=$(realpath "$script_dir/../..")

cd $prj_dir

# Get the name of the current checked out branch or the commit if the repo is checkout at a commit
rev_to_use=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse HEAD)

# Extract the GitHub Project name from the remote URL using regex
github_prj_name=$(git remote get-url origin | grep -oP "(?<=.com[:/]).*")

# Get the manifest file automatically
manifest_file=$(find "$prj_dir" -maxdepth 1 -type f -name "*.xml")

if command -v "repo" >/dev/null 2>&1; then
    set -x
    # Execute the command for the repo init in order to initialize the repo
    repo init -u ssh://git@github.ford.com/$github_prj_name -m $manifest_file -b $rev_to_use -c

    # Execute the command for repo sync so all the dependencies are downloaded
    repo sync --verbose --current-branch
    set +x
else
    echo "Google Repo is not installed!! Follow the instructions at \"https://github.ford.com/FNV4-FordOS/git-repo_googlesource\" for installation"
    exit 1
fi


