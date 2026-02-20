#!bin/bash

#add all files
git add .

# add commit message
echo "Add Commit Message: "
read message

git commit -m "$message"

git push
