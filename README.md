# git_svn_externals
git svn externals simple tool


# how to use

    $ git svn show-externals > git_svn_externals.list
    $ ## edit git_svn_externals.list file.
    $ git-svn-externals.py checkout git_svn_externals.list
    $ git-svn-externals.py update git_svn_externals.list
    $ git-svn-externals.py status git_svn_externals.list
    $ git-svn-externals.py revert git_svn_externals.list


# future todo
  * run into repo sub directory. 
  * run from 'git svn show-externals' command
  * run with svn external a file not a directory.
  * ...
