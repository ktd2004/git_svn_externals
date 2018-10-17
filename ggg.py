#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import sys
import shutil
import subprocess



def git_find_root(tdir):
    curdir = tdir
    while True:
        if os.path.isdir(os.path.join(curdir, ".git")):
            return curdir
        parent = os.path.normpath(os.path.join(curdir, ".."))
        if os.path.normpath(curdir) == os.path.normpath(parent):
            return ""
        curdir = parent


def git_svn_url(tdir):
    os.chdir(tdir)

    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    p = subprocess.Popen("git svn info".split(), env=my_env, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return ""

    for line in out.splitlines():
        if line.startswith("URL: "):
            return line.split(' ', 1)[1]


def git_ls_files(tdir):
    os.chdir(tdir)

    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    p = subprocess.Popen("git ls-files".split(), env=my_env, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return []

    dirs = set()
    for line in out.splitlines():
        dirs.add(os.path.dirname(line))
    return list(dirs)


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


def git_svn_get_externals(tdir):
    os.chdir(tdir)

    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    FNULL = open(os.devnull, "w")
    p = subprocess.Popen("git svn propget svn:externals".split(), env=my_env, stdout=subprocess.PIPE, stderr=FNULL)
    out, err = p.communicate()
    if err:
        return []
    
    extinfo = []
    for line in out.splitlines():
        if line:
            extinfo.append(line.split(' ', 1))

    return extinfo


def svn_checkout(tardir, svnurl, extinfo):
    #print(tardir)
    #print(svnurl)
    #print(extinfo)
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if os.path.exists(abspath):
            print("[error] %s is already exist." % abspath)
            continue
        svnuuu = svn_path_normpath(svnurl + '/' + exi[0])
        cmd = "svn checkout %s %s" % (svnuuu, abspath)
        #print(cmd)
        os.system(cmd)


def svn_switch(tardir, svnurl, extinfo):
    #print(tardir)
    #print(svnurl)
    #print(extinfo)
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        svnuuu = svn_path_normpath(svnurl + '/' + exi[0])
        cmd = "svn switch %s %s" % (svnuuu, abspath)
        #print(cmd)
        os.system(cmd)


def svn_update(tardir, svnurl, extinfo):
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn update %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_status(tardir, svnurl, extinfo):
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn status %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_info(tardir, svnurl, extinfo):
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn info %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_revert(tardir, svnurl, extinfo):
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn revert -R %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_remove(tardir, svnurl, extinfo):
    print("remove list:\n")
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            continue
        print('\t' + abspath)

    ans = raw_input("\nAre you sure remove the list[y/n]?")
    if ans != 'y' and ans != "yes":
        return

    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            continue
        if os.path.isdir(abspath):
            shutil.rmtree(abspath)
        else:
            os.remove(abspath)


def svn_list(tardir, svnurl, extinfo):
    #print(tardir)
    #print(svnurl)
    #print(extinfo)
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        print(abspath)


def printHelp():
    print("git-svn-externals.py : git svn externals tools")
    print("[usage] git-svn-externals.py subcommand [PATH]")
    print("subcommand")
    print("    checkout|co :")
    print("    switch|sw   :")
    print("    update|up   :")
    print("    status|st   :")
    print("    info        :")
    print("    revert      :")
    print("    remove      :")
    print("    list        :")


if __name__ == "__main__":
    curdir = os.getcwd()
    argc = len(sys.argv)
    if argc == 1:
        printHelp()
        sys.exit(0)
    elif argc == 2:
        tardir = curdir
    elif argc == 3:
        tardir = os.path.abspath(sys.argv[2])
    else:
        print("[error] invalid argument count.")
        sys.exit(1)

    command = sys.argv[1]
    if not os.path.exists(tardir):
        print("[error] target directory is not exist.")
        sys.exit(1)

    rootdir = git_find_root(curdir)
    if not rootdir:
        print("[error] is not git repository.")
        sys.exit(1)

    rootdir = git_find_root(tardir)
    if not rootdir:
        print("[error] is not git repository.")
        sys.exit(1)


    print("curdir : ", curdir)
    print("tardir : ", tardir)
    print("rootdir : ", rootdir)


    svnurl = git_svn_url(rootdir)
    if not svnurl:
        print("[error] git svn info command error.")
        sys.exit(1)

    svnurl = svn_path_normpath(svnurl + tardir.replace(rootdir, ""))
    print("svnurl : ", svnurl)

    dirs = git_ls_files(tardir)
    print(dirs)
    for dir in dirs:
        tdir = os.path.join(tardir, dir)
        extinfo = git_svn_get_externals(tdir)
        print(extinfo)
        if not extinfo:
            continue

        if command in ["checkout", "co"]:
            svn_checkout(tdir, svnurl, extinfo)
        elif command in ["switch", "sw"]:
            svn_switch(tdir, svnurl, extinfo)
        elif command in ["update", "up"]:
            svn_update(tdir, svnurl, extinfo)
        elif command in ["status", "st"]:
            svn_status(tdir, svnurl, extinfo)
        elif command in ["info"]:
            svn_info(tdir, svnurl, extinfo)
        elif command in ["revert"]:
            svn_revert(tdir, svnurl, extinfo)
        elif command in ["remove"]:
            svn_remove(tdir, svnurl, extinfo)
        elif command in ["list"]:
            svn_list(tdir, svnurl, extinfo)
        else:
            print("[error] invalid subcommand.")
            sys.exit(1)

    sys.exit(0)
