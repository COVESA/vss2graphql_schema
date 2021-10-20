# Installation of utilities

## Git Hooks

The git hooks will prevent the commit or push of files that do not comply
with some criteria.

Sample files are located at `.git/hooks` with `.sample` extension and are not
read.

The hook files of this project are located at `utils/git`. They
can be installed with by executing the script `./git/install-git-hooks.sh`
that will create a symbolic link at `.git/hooks` to this files.
