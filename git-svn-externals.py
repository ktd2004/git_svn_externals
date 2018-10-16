#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 user <user@ubuntu>
#
# Distributed under terms of the MIT license.
import sys
import os
import shutil
import subprocess



## 방법
# 1. git repo root에서 시작해야함. .git 디렉토리 확인
# 2. svnurl = git svn info | sed ...
# 3. checkout인지? update? revert? status? 인지 subcommand 입력
# 4. git-svn-external 정보 파일 읽기
# 5. loop를 돌면서 명령 수행
# 6. cd [0] svn co svnurl+[1] [2]


def git_svn_url():
    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    p = subprocess.Popen("git svn info".split(), env=my_env, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return ""

    for line in out.splitlines():
        if line.startswith("URL: "):
            return line.split(' ', 1)[1]


def git_svn_find_root(cur):
    rootdir = cur
    while True:
        if os.path.isdir(os.path.join(rootdir, ".git")):
            return rootdir
        os.chdir("..")
        parent = os.path.abspath(os.curdir)
        if rootdir == parent:
            return ""
        rootdir = parent



def read_git_svn_show_externals(inf):
    basedir = ""
    extinfo = []

    while True:
        line = inf.readline()
        if not line: break

        line = line.strip()

        if line == "":
            basedir = ""
        if line.startswith("#"):
            basedir = line.split(' ', 1)[1]
        else:
            if basedir != "":
                extinfo.append([basedir, line.split(' ', 1)])

    return extinfo



def svn_path_normpath(svnpath):
    str = ""
    if svnpath.startswith("svn:/"):
        str = "svn:/" + os.path.normpath(svnpath[5:])
    elif svnpath.startswith("svn+ssh:/"):
        str = "svn+ssh:/" + os.path.normpath(svnpath[9:])
    elif svnpath.startswith("file:/"):
        str = "file:/" + os.path.normpath(svnpath[6:])
    elif svnpath.startswith("http:/"):
        str = "http:/" + os.path.normpath(svnpath[6:])
    elif svnpath.startswith("https:/"):
        str =  "https:/" + os.path.normpath(svnpath[7:])
    else:
        return ""

    return str.replace(os.sep, '/')


def svn_checkout(rootdir, svnurl, extinfo):
    for pp in extinfo:
        abspath = os.path.join(rootdir, pp[0][1:])
        if not os.path.exists(abspath):
            os.makedirs(abspath)
        os.chdir(abspath)
        svnuuu = svn_path_normpath(svnurl + pp[1][0])
        cmd = "svn checkout %s %s" % (svnuuu, pp[1][1])
        os.system(cmd)


def svn_update(rootdir, svnurl, extinfo):
    for pp in extinfo:
        abspath = os.path.join(rootdir, pp[0][1:])
        os.chdir(abspath)
        cmd = "svn update %s" % pp[1][1]
        os.system(cmd)


def svn_switch(rootdir, svnurl, extinfo):
    for pp in extinfo:
        abspath = os.path.join(rootdir, pp[0][1:])
        os.chdir(abspath)
        svnuuu = svn_path_normpath(svnurl + pp[1][0])
        cmd = "svn switch %s %s" % (svnuuu, pp[1][1])
        os.system(cmd)


def svn_status(rootdir, svnurl, extinfo):
    for pp in extinfo:
        abspath = os.path.join(rootdir, pp[0][1:])
        os.chdir(abspath)
        cmd = "svn status %s" % pp[1][1]
        os.system(cmd)


def svn_remove(rootdir, svnurl, extinfo):
    print("remove list:\n")
    for pp in extinfo:
        abspath = os.path.join(rootdir, pp[0][1:], pp[1][1])
        fullpath = os.path.normpath(abspath)
        print('\t' + fullpath)

    ans = raw_input("\nAre you sure remove the list[y/n]?")
    if ans == 'y' or ans == "yes":
        for pp in extinfo:
            abspath = os.path.join(rootdir, pp[0][1:], pp[1][1])
            fullpath = os.path.normpath(abspath)
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
            else:
                os.remove(fullpath)


def svn_revert(rootdir, svnurl, extinfo):
    for pp in extinfo:
        abspath = os.path.join(rootdir, pp[0][1:])
        os.chdir(abspath)
        cmd = "svn revert -R %s" % pp[1][1]
        os.system(cmd)


def svn_info(rootdir, svnurl, extinfo):
    for pp in extinfo:
        abspath = os.path.join(rootdir, pp[0][1:])
        os.chdir(abspath)
        cmd = "svn info %s" % pp[1][1]
        os.system(cmd)


def svn_list(rootdir, svnurl, extinfo):
    for pp in extinfo:
        path = os.path.normpath(os.path.join(rootdir, pp[0], pp[1][1]))
        print(path)


def printHelp():
    print("[info] git svn externals tool")
    print("[usage] git-svn-externals.py subcommand git_svn_show_externals_file")
    print("subcommand")
    print("    checkout|co : ")
    print("    update|up : ")
    print("    switch|sw : ")
    print("    status|st : ")
    print("    remove|rm : ")
    print("    revert : ")
    print("    info : ")
    print("    list : ")
    print("input from file or stdin")
    print("    git-svn-externals.py subcommand git_svn_show_externals_file")
    print("    git svn show-externals | git-svn-externals.py subcommand -")




if __name__ == "__main__":

    # 선행 조건 체크
    # parameter count
    # git repo and root

    argc = len(sys.argv)
    if argc == 1:
        printHelp()
        sys.exit(0)

    if argc != 3:
        print("[error] invalid argument")
        sys.exit(1)

    svnurl = git_svn_url()
    if not svnurl:
        print("[error] git svn error")
        sys.exit(1)

    curdir = os.getcwd()
    rootdir = git_svn_find_root(curdir)
    command = sys.argv[1]
    filepath = sys.argv[2]
    if filepath == "-":
        inf = sys.stdin
    else:
        inf = open(filepath, "r")


    #print("svnurl : ", svnurl)
    #print("rootdir : ", rootdir)

    if not svnurl or rootdir == "":
        print("[error] is not git_svn_repo or git_svn_repo_root")
        sys.exit(1)

    extinfo = read_git_svn_show_externals(inf)

    #for ll in extinfo:
    #    print(ll)

    if command == "checkout" or command == "co":
        svn_checkout(rootdir, svnurl, extinfo)
    elif command == "update" or command == "up":
        svn_update(rootdir, svnurl, extinfo)
    elif command == "switch" or command == "sw":
        svn_switch(rootdir, svnurl, extinfo)
    elif command == "status" or command == "st":
        svn_status(rootdir, svnurl, extinfo)
    elif command == "remove" or command == "rm":
        svn_remove(rootdir, svnurl, extinfo)
    elif command == "revert":
        svn_revert(rootdir, svnurl, extinfo)
    elif command == "info":
        svn_info(rootdir, svnurl, extinfo)
    elif command == "list":
        svn_list(rootdir, svnurl, extinfo)
    else:
        print("[error] invalid subcommand")

    sys.exit(0)
