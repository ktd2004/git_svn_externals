# git_svn_externals
git svn externals simple tool


# how to use

    $ git svn show-externals > git_svn_externals.list
    $ ## edit git_svn_externals.list file.
    $ git-svn-externals.py checkout git_svn_externals.list
    $ git-svn-externals.py update git_svn_externals.list
    $ git-svn-externals.py status git_svn_externals.list
    $ git-svn-externals.py remove git_svn_externals.list


    $ git svn show-externals | git-svn-externals.py checkout -
    $ git svn show-externals | git-svn-externals.py update -
    $ git svn show-externals | git-svn-externals.py status -
    $ git svn show-externals | git-svn-externals.py remove -


# future todo
  * run with svn external a file not a directory.
  * ...
