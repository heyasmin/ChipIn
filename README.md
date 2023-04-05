# jamee
A website/ dashboard for personal financial tracking

## Before Coding

- PULL the most recent version of the code
- STATUS to check which branch you are currently on
- CHECKOUT -b will create a new branch and switch you on to that branch

OR

- CHECKOUT (without -b) will switch you between the branches

```bash
git pull
git status

git checkout -b the_name_of_your_branch
OR
git checkout the_name_of_your_branch
```

## To upload your code
```bash
git add the_filename
git commit -m "your_message"
git push origin
```

## To create a 'pull request' so you can merge your branch with the main and have others review the code.

- navigate to the repo on the web
- go to your branch where you have uploaded the code
![Find your branch](application/static/branch.jpg)
- click the green pull request button
- add the pull request and tag the reviewers, tag yourself as an assignee and tag the project so we see it on the board
![Create pull request](application/static/pull_rqst.jpg)
