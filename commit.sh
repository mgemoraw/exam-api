#!/usr/bin/bash

#add all files
git add .

# add commit message
echo "Add Commit Message: "
read message

git commit -m "$message"
echo "All changes have been committed successfully!"

echo "Pushing changes to remote repository..."
git push

echo "All changes have been pushed successfully!"
