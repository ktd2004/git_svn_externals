#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import sys
import subprocess



def git_find_root(tdir):
    os.chdir(tdir)
    curdir = tdir
    while True:
        if os.path.isdir(os.path.join(curdir, ".git")):
            return curdir
        os.chdir("..")
        parent = os.path.abspath(os.curdir)
        if curdir == parent:
            return ""
        curdir = parent


def git_svn_url(tdir):
    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    cmd = "git svn info %s" % tdir

    p = subprocess.Popen(cmd.split(), env=my_env, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return ""

    for line in out.splitlines():
        if line.startswith("URL: "):
            return line.split(' ', 1)[1]


def git_ls_files(tdir):
    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    cmd = "git ls-files %s" % tdir
    p = subprocess.Popen(cmd.split(), env=my_env, stdout=subprocess.PIPE)
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
    my_env = os.environ.copy()
    my_env["LANG"] = "C"

    cmd = "git svn propget svn:externals %s" % tdir
    FNULL = open(os.devnull, "w")
    p = subprocess.Popen(cmd.split(), env=my_env, stdout=subprocess.PIPE, stderr=FNULL)
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
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        if not os.path.exists(abspath):
            print("[error] %s is not exist." % abspath)
            continue
        cmd = "svn revert -R %s" % abspath
        #print(cmd)
        os.system(cmd)


def svn_list(tardir, svnurl, extinfo):
    #print(tardir)
    #print(svnurl)
    #print(extinfo)
    for exi in extinfo:
        abspath = os.path.join(tardir, exi[1])
        print(abspath)



if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        printHelp()
        sys.exit(0)

    if argc != 3:
        print("[error] invalid argument count.")
        sys.exit(1)

    command = sys.argv[1]
    tardir = os.path.abspath(sys.argv[2])
    #print("tardir : ", tardir)
    if not os.path.exists(tardir):
        print("[error] target directory is not exist.")
        sys.exit(1)

    curdir = os.getcwd()
    #print("curdir : ", curdir)
    rootdir = git_find_root(tardir)
    #print("rootdir : ", rootdir)
    if not rootdir:
        print("[error] is not git repository.")
        sys.exit(1)

    svnrooturl = git_svn_url(rootdir)
    #print("svnrooturl : ", svnrooturl)
    svnurl = git_svn_url(tardir)
    #print("svnurl : ", svnurl)
    if not svnrooturl or not svnurl:
        print("[error] git svn info command error.")
        sys.exit(1)

    dirs = git_ls_files(tardir)
    #print(dirs)
    for dir in dirs:
        extinfo = git_svn_get_externals(dir)
        #print(extinfo)
        if not extinfo:
            continue

        if command in ["checkout", "co"]:
            svn_checkout(dir, svnurl, extinfo)
        elif command in ["switch", "sw"]:
            svn_switch(dir, svnurl, extinfo)
        elif command in ["update", "up"]:
            svn_update(dir, svnurl, extinfo)
        elif command in ["status", "st"]:
            svn_status(dir, svnurl, extinfo)
        elif command in ["info"]:
            svn_info(dir, svnurl, extinfo)
        elif command in ["revert"]:
            svn_revert(dir, svnurl, extinfo)
        elif command in ["remove"]:
            svn_remove(dir, svnurl, extinfo)
        elif command in ["list"]:
            svn_list(dir, svnurl, extinfo)
        else:
            print("[error] invalid subcommand.")
            sys.exit(1)

    sys.exit(0)
