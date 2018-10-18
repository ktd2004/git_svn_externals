# git_svn_externals

gse.py is simple tool


# how to use

    $ cd git_repo
    $ gse.py {checkout|co} path
    $ gse.py {switch|sw} path
    $ gse.py {update|up} path
    $ gse.py {status|st} path
    $ gse.py revert path


# read svn:externals information from file or STDIN

    $ git svn propget svn:externals . > svn_externals.txt
    $ gse.py co . svn_externals.txt
    $ git svn propget svn:externals . | gse.py co . -
